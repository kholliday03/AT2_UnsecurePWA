from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
from werkzeug.security import generate_password_hash
import sqlite3
import os
import user_management as dbHandler

app = Flask(__name__)
app.secret_key = "SftEng-SSA-AT2"

@app.route("/index.html", methods=["POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn, user = dbHandler.retrieveUsers(username, password)    # Need to have a retrieveUsers() function in user_management.py
        if isLoggedIn:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            dbHandler.listFeedback()    # Need to have a listFeedback() function in user_management.py
            return redirect(url_for("success"))
    
    return render_template("index.html")    # Retry login process

@app.route("/signup.html", methods=["POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        dob = request.form["dob"]   # Use the "dateofbirth" type in the template
        try:
            dbHandler.insertUser(username, password, dob)
        except sqlite3.IntegrityError:
            return render_template("signup.html")
        return redirect(url_for("index"))
    
    return render_template("signup.html")

app.run(debug=True, port=5000)