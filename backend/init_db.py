
import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False, timeout=10)

#execute sql script to create user table
with open('userSchema.sql') as f:
    conn.executescript(f.read())

with open('profileSchema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()


#initialize user table with test entry
cur.execute("INSERT INTO user (username, email, userpassword) VALUES (?, ?, ?)", 
    ('testuser', 'test@test', 'test'))

conn.commit()
conn.close()

