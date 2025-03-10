import re
from datetime import datetime

from flask import Flask
from flask import render_template, render_template_string
from flask import request
from flask_mysqldb import MySQL

import folium
import folium.map


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'crash'
app.config['MYSQL_PASSWORD'] = 'crash'
app.config['MYSQL_DB'] = 'robiot'

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM BaimenMotak''')
    results = cur.fetchall()
    return str(results)
#    return "Hello, Flask!"

@app.route("/hello/<name>", methods=["GET", "POST"])
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

@app.route("/map", methods=["GET", "POST"])
def map():
    """Embed a map as an iframe on a page."""
    m = folium.Map()
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()


    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )
    