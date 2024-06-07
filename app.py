import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,g

# Configure application
app = Flask(__name__)
app.secret_key = "your_secret_key"
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ourdb.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['username'] = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO user (un, pss) VALUES (:username, :password)",
                    username=session['username'], password=password)
        db.execute("create table IF NOT EXISTS :username (name TEXT,month int, year int)",username=session['username'])
        year = datetime.now()
        rows = db.execute(f"SELECT * FROM :username", username=session['username'])

        return render_template("index.html", rows=rows, year=year)
    else:
        return render_template("login.html")


@app.route("/doc", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        yaer = request.form.get("year")
        year = datetime.now()

        #insert info
        db.execute("INSERT INTO :username (name, year, month ) VALUES (:name, :year ,:month)",
                    username= session['username'],name=name, month=month, year=yaer)
        return redirect("/doc")
    else:
        year = datetime.now()
        rows = db.execute(f"SELECT * FROM :username", username=session['username'])
        return render_template("index.html", rows=rows, year=year)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        return redirect("/doc")
    else:
        return render_template("upload.html")

