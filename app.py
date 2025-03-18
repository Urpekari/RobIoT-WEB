import re
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template, Response, session
from flask_mysqldb import MySQL
from model.model import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'RobIoT'
app.config['MYSQL_PASSWORD'] = 'RobIoT'
app.config['MYSQL_DB'] = 'robiot'

mysql=MySQL(app)

dboutput=output(mysql)
dbinput=input(mysql)

@app.route("/")
def index():
    return render_template(
        "root.html"
    )

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['erabiltzailea']
    password = request.form['pasahitza']
    
    if dboutput.erabiltzailea_egiaztatu(username, password): #llama a la funcion de arriba q mira en la base de datos
        #session['usuario'] = username #guarda el usuario en session que es como una memoria temporal del flask
        return redirect(url_for('database_show')) #manda al usuario a la siguiente pagina, en este caso dashboard
    else:
        return "Usuario o contraseña incorrectos", 401 #401 es el código de estado HTTP para "No autorizado".

@app.route("/database")
def database_show():
    return render_template(
        "database.html",
        header=tables.Droneak_header,
        items=dboutput.get_info(tables.Droneak)
    )

@app.route("/database/dowload")
def download_csv():
    csv = dboutput.create_csv(tables.Droneak)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Erabiltzaileak.csv"})

@app.route("/database/insert",methods=['POST'])
def in_drone():
    info=(request.form["izena"],request.form["mota"],request.form["deskribapena"])
    dbinput.insert_Droneak(info)
    return redirect(url_for("database_show")) 


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