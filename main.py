from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape   # Used to prevent XSS.
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

@app.route("/success.html", methods=["GET", "POST"])
def addFeedback():
    if request.method == "POST":
        feedback = escape(request.form["feedback"]) # Using the escape function to sanitise data / prevent XSS - prevents the storage of dangerous characters in the database.
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return redirect(url_for("success"))
    else:
        dbHandler.listFeedback()
        return redirect(url_for("success"))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(host='0.0.0.0', port=5000)