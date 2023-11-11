import sqlite3
import config

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO fitbit_auth (user_id, access_token) VALUES (?, ?)",
            (config.user_id, config.access_token)
            )

connection.commit()
connection.close()