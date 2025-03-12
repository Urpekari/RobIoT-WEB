import re
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template, Response
from flask_mysqldb import MySQL
import database

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'RobIoT'
app.config['MYSQL_PASSWORD'] = 'RobIoT'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template(
        "root.html"
    )

@app.route("/database")
def database_show():
    return render_template(
        "database.html",
        header=database.Erabiltzaileak_header,
        items=database.get_info(mysql,database.Erabiltzaileak)
    )

@app.route("/database/dowload")
def download_csv():
    csv = database.create_csv(mysql,database.Erabiltzaileak)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Erabiltzaileak.csv"})

#@app.route("/hello/<name>")
#def hello_there(name):
#    now = datetime.now()
#    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
#    match_object = re.match("[a-zA-Z]+", name)

#    if match_object:
#        clean_name = match_object.group(0)
#    else:
#        clean_name = "Friend"

#    content = "Hello there, " + clean_name + "! It's " + formatted_now
#    return content

@app.route("/hello/", methods=['POST'])
def hello():
    name=request.form["name"]
    return redirect(url_for("hello_there",name=name))

@app.route("/hello/<name>")
def hello_there(name):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )