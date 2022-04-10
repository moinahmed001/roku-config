import sqlite3
import datetime
import requests

# Future enhancement, pass these as an array instead to save processing
# though it only runs once a day so it's not exactly important.
def insertVariableIntoTable(datetime, date, consumption):
    try:
        sqliteConnection = sqlite3.connect('octoprice.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO 'gasprices'
			('datetime', 'date', 'consumption')
                        VALUES (?, ?, ?);"""

        data_tuple = (datetime, date, consumption)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("1 record inserted successfully into gasprices table")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into gasprices table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed. We are done here.")


response = requests.get('https://api.octopus.energy/v1/gas-meter-points/7680711609/meters/E6S14525412061/consumption/', auth=('sk_live_xL8q1cUYWnc4cOgpR0X0iwMm', ''))

pricedata = response.json()

for result in pricedata['results']:
    consumption = result['consumption']
    interval_start = result['interval_start']
    date_formatted = datetime.datetime.strptime(interval_start, "%Y-%m-%dT%H:%M:%S%z")
    mom_year = (date_formatted.year)
    month = (date_formatted.month)
    day = (date_formatted.day)
    if month < 10:
        month = "0{0}".format(month)
    if day < 10:
        day = "0{0}".format(day)

    date = str(mom_year) + "-" + str(month) + "-" + str(day)

    insertVariableIntoTable(interval_start, date, consumption)
