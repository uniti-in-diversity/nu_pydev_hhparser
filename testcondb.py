import sqlite3

data = 'астрахань'
conn = sqlite3.connect('hhdb.db')
cursor = conn.cursor()

cursor.execute('INSERT INTO test (name) VALUES (?)', ([data]))
conn.commit()

cursor.execute('SELECT * from test')