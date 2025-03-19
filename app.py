import re
from datetime import datetime

from flask import Flask
from flask import render_template, render_template_string
from flask import request
from flask_mysqldb import MySQL

import env

from view.droneControlPage import *



app = Flask(__name__)

#TODO: LORTU DRONEID DINAMIKOKI
droneID = 0

# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

app.config['MYSQL_HOST'] = env.mysql_host_ip
app.config['MYSQL_USER'] = env.mysql_username
app.config['MYSQL_PASSWORD'] = env.mysql_password
app.config['MYSQL_DB'] = env.mysql_db_name

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM BaimenMotak''')
    results = cur.fetchall()
    return str(results)
#    return "Hello, Flask!"

@app.route("/map", methods=["GET", "POST"])
def callMap():
    print(droneID)
    page = mapPage(droneID)
    content = page.map(droneID)
    return content