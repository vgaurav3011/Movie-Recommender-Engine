import sqlite3 as sql

def insert(username,email,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO register (username,email,password) VALUES (?,?,?)", (username,email,password))
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()
