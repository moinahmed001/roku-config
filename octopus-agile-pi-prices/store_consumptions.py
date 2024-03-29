# this is the one to run daily just after 4pm ish when the new prices come in
agile_tariff_code = 'E-1R-AGILE-18-02-21-A'  # This changes by area so choose the right one (displayed in your octopus dashboard). Codes end in A->P

# curl -u "sk_live_xL8q1cUYWnc4cOgpR0X0iwMm:" "https://api.octopus.energy/v1/electricity-meter-points/1050001232117/meters/20L3751053/consumption/"

import sqlite3
import datetime
import requests
# from store_prices import insertVariableIntoTable

# Future enhancement, pass these as an array instead to save processing
# though it only runs once a day so it's not exactly important.
def insertOrUpdateVariableIntoTable(datetime, consumption):
    try:
        sqliteConnection = sqlite3.connect('octoprice.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        print("UPDATE prices SET consumption = {0} WHERE datetime = {1}".format(consumption, datetime))
        cursor.execute('''UPDATE prices SET consumption = ? WHERE datetime = ?''', (consumption, datetime))
        sqliteConnection.commit()
        if cursor.rowcount > 0:
            print("Total", cursor.rowcount, "Records updated successfully")
        else:
            print("Total", cursor.rowcount, "Records updated successfully")

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into prices table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed. We are done here.")

# i = 1
# while i < 40:
    # print('>>>>>' + 'https://api.octopus.energy/v1/electricity-meter-points/1012365897569/meters/16K0245801/consumption/?page='+str(i))
response = requests.get('https://api.octopus.energy/v1/electricity-meter-points/1012365897569/meters/16K0245801/consumption/', auth=('sk_live_l9L4iBkcPXPtCAg2QsUmiQb8', ''))
# response = requests.get('https://api.octopus.energy/v1/electricity-meter-points/1012365897569/meters/16K0245801/consumption/?page='+str(i), auth=('sk_live_l9L4iBkcPXPtCAg2QsUmiQb8', ''))
pricedata = response.json()
for result in pricedata['results']:
	consumption = result['consumption']
	raw_from = result['interval_start'].replace('+01:00','Z')
	print(raw_from)
	print(consumption)
	insertOrUpdateVariableIntoTable(raw_from, consumption)

    # i += 1

# consumption = pricedata['results'][0]['consumption']
# raw_from = pricedata['results'][0]['interval_start']
# print("consumption 1: ", consumption, ", raw_from: ", raw_from)
#
# insertOrUpdateVariableIntoTable(raw_from, consumption)
#
# consumption = pricedata['results'][1]['consumption']
# raw_from = pricedata['results'][1]['interval_start']
# print("consumption 2: ", consumption, ", raw_from: ", raw_from)
#
# insertOrUpdateVariableIntoTable(raw_from, consumption)

#print(pricedata)
