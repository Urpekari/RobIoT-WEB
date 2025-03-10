import re
from datetime import datetime

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'RobIoT'
app.config['MYSQL_PASSWORD'] = 'RobIoT'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM baimenmotak''')
    results = cur.fetchall()
    return str(results)
#    return "Hello, Flask!"


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content