# this is the one to run daily just after 4pm ish when the new prices come in
agile_tariff_code = 'E-1R-AGILE-18-02-21-A'  # This changes by area so choose the right one (displayed in your octopus dashboard). Codes end in A->P

import sqlite3
import datetime
import requests

# Future enhancement, pass these as an array instead to save processing
# though it only runs once a day so it's not exactly important.
def insertVariableIntoTable(datetime, date, price):
    try:
        sqliteConnection = sqlite3.connect('octoprice.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO 'prices'
			('datetime', 'date', 'price')
                        VALUES (?, ?, ?);"""

        data_tuple = (datetime, date, price)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("1 record inserted successfully into prices table")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into prices table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed. We are done here.")


response = requests.get('https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/'+agile_tariff_code+'/standard-unit-rates/')
pricedata = response.json()
# print(pricedata['results'][0]['value_inc_vat'])
# mom_price = pricedata['results'][0]['value_inc_vat']
# raw_from = pricedata['results'][0]['valid_from']
# insertVariableIntoTable(raw_from, mom_price)
# mom_price = pricedata['results'][1]['value_inc_vat']
# raw_from = pricedata['results'][1]['valid_from']
# insertVariableIntoTable(raw_from, mom_price)

for result in pricedata['results']:
    mom_price = result['value_inc_vat']
    raw_from = result['valid_from']
    date_formatted = datetime.datetime.strptime(raw_from, "%Y-%m-%dT%H:%M:%SZ")
    mom_year = (date_formatted.year)
    mom_month = (date_formatted.month)
    mom_day = (date_formatted.day)

    date = str(mom_year) + "-" + str(mom_month) + "-" + str(mom_day)
    insertVariableIntoTable(raw_from, date, mom_price)
