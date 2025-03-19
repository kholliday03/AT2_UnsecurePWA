import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    user = cur.execute(f"SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user and check_password_hash(user["password"], password) and cur.fetchone() != None:
        # Plain text log of visitor count as requested by Unsecure PWA management - no change required.
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number)) 
        con.close()
        return True, user
    con.close()
    return False, False

def insertUser(username, password, dob):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth) VALUES (?,?,?)",
        (username, generate_password_hash(password), dob)
    )
    con.commit()
    con.close()