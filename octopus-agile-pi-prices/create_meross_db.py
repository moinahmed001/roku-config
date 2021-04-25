# sets up the db; run this script once. ever.

import sqlite3

conn = sqlite3.connect('octoprice.sqlite')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS meross (deviceName TEXT, routineTime TEXT, switch TEXT, PRIMARY KEY (deviceName, routineTime))')
conn.commit()
conn.close()
