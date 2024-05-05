import sqlite3

conn = sqlite3.connect("dairy.db")
c = conn.cursor()
try:
    c.execute("create table diary (datetime, content)")
    print("done")
except sqlite3.OperationalError:
    print("done")