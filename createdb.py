import sqlite3

conn = sqlite3.connect("Messages.db")

c = conn.cursor()

c.execute("INSERT INTO messages VALUES ('today', 'message5')")
conn.commit()
conn.close()
