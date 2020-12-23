# sets up the db; run this script once. ever.

import sqlite3

conn = sqlite3.connect('octoprice.sqlite')

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS prices (datetime TEXT PRIMARY KEY, date TEXT, price REAL, consumption NUMBER)')
conn.commit()
conn.close()
