from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import sqlite3
import os
import user_management as dbHandler

app = Flask(__name__)
app.secret_key = "SftEng-SSA-AT2"

def get_db(): 
    db = sqlite3.connect('database/database.db') 
    db.row_factory = sqlite3.Row 
    return db

@app.route("/index.html", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)    # Need to have a retrieveUsers() function in user_management.py
        if isLoggedIn:
            session.clear()
            # Continue entering a session
            dbHandler.listFeedback()    # Need to have a listFeedback() function in user_management.py
            # Continue from here

app.run(debug=True, port=5000)