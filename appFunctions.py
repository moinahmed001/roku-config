import time, re
import delegator, json
from getter import *
from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3
from decimal import Decimal

def consumption_data():
    result = []
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM 'prices' order by date(date) DESC;""")

    rows = cur.fetchall()
    for row in rows:
        result.append({'datetime': row[0], 'date': row[1], 'price': row[2], 'consumption': row[3]})

    return result

def consumption_data_daily():
    result = []
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""SELECT date from 'prices' group by date order by date(date) DESC limit 1,7;""")
    # cur.execute("""SELECT date from 'prices' where consumption is not NULL group by date order by date(date) DESC;""")

    rows = cur.fetchall()
    for row in rows:
        consumption_date = row[0]
        daily_total = fetch_daily_consumption(consumption_date)
        daily_total["average"]= fetch_daily_consumption_average(consumption_date)
        result.append(daily_total)
    return result

def fetch_daily_consumption(consumption_date):
    conn = create_connection()
    cur2 = conn.cursor()
    sql_select_query = """SELECT price, consumption from 'prices' where date = ?;"""
    # sql_select_query = """SELECT price, consumption from 'prices' where date = ? AND consumption > 0;"""
    cur2.execute(sql_select_query, (consumption_date,))

    all_rows = cur2.fetchall()
    daily_total = 21
    kwh = 0
    for cost in all_rows:
        price = cost[0]
        consumption = 0
        if cost[1]:
            consumption = cost[1]

        daily_total = daily_total + (price * consumption)
        kwh = kwh + consumption

    total = round(Decimal(daily_total/100), 2)

    return {'date': consumption_date, 'cost': Decimal(total), 'kwH': Decimal(round(Decimal(kwh), 2))}


def fetch_daily_consumption_average(consumption_date):
    conn = create_connection()
    cur2 = conn.cursor()
    sql_select_query = """SELECT count(datetime), sum(price) from 'prices' where date = ? and datetime not like '%T16:%' and datetime not like '%T17:%' and datetime not like '%T18:%';"""
    cur2.execute(sql_select_query, (consumption_date,))

    all_rows = cur2.fetchall()
    total = 0
#    print(all_rows[0][1])
    if all_rows:
        average = all_rows[0][1]/all_rows[0][0]
        total = round(Decimal(average/100), 2)

    return Decimal(total)


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('octopus-agile-pi-prices/octoprice.sqlite')
    except sqlite3.Error as e:
        print(e)

    return conn

def updated_tariff_data():
    tariffs = get_tariff_data()["results"]
    # insert them all into the db
    updated_tariff = []
    for tariff in reversed(tariffs):
        if "value_exc_vat" in tariff:
            del tariff["value_exc_vat"]

        if its_in_the_future(tariff["valid_to"]):
            tariff_with_date = readable_date(tariff)
            updated_tariff.append(tariff_with_date)
    return updated_tariff

def readable_date(tariff):
    valid_from = datetime.datetime.strptime(tariff["valid_from"], "%Y-%m-%dT%H:%M:%SZ")
    valid_to = datetime.datetime.strptime(tariff["valid_to"], "%Y-%m-%dT%H:%M:%SZ")

    tariff["time"] = valid_from.strftime("%d %h: %H:%M")
    return tariff

def its_in_the_future(valid_date):
    present = datetime.datetime.now()
    given_date = datetime.datetime.strptime(valid_date, "%Y-%m-%dT%H:%M:%SZ")
    return given_date > present



def get_tariff_data():
    url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-A/standard-unit-rates/"
    response = requests.get(url)
    return json.loads(response.content)


def all_config_hash():
    live_config_hash = {}
    all_urls = [
    "https://www.nowtv.com/gb/watch/home", "https://www.nowtv.com/ie/watch/home", "https://skyticket.sky.de/watch/home", "https://www.nowtv.it/watch/home", "https://www.sky.es/ver/inicio"
    ]

    for url in all_urls:
        raw_html = simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')
        string_html = raw_html.decode("utf-8").split()
        release_hash = 'UNKNOWN'

        for aString in string_html:
            if "href" in aString:
                hash = re.findall(r'static\/(.*?)\/core', aString)
                if len(hash) == 1:
                    release_hash = hash[0]
                    live_config_hash[url] = hash[0]
                    break

    return live_config_hash


def tv_is_off():
    p = delegator.run('vcgencmd display_power')
    if "=0" in p.out:
        return True
    else:
        return False
