import re
from datetime import datetime

from flask import *
from flask_mysqldb import MySQL

import env
from view.droneControlPage import *
from model.model import *


app = Flask(__name__)

#TODO: LORTU DRONEID DINAMIKOKI
droneID = 1

# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

app.config['MYSQL_HOST'] = env.mysql_host_ip
app.config['MYSQL_USER'] = env.mysql_username
app.config['MYSQL_PASSWORD'] = env.mysql_password
app.config['MYSQL_DB'] = env.mysql_db_name
app.secret_key = 'hackerdeminecraft'

mysql=MySQL(app)

dboutput=output(mysql)
dbinput=input(mysql)

def getDBOutput():
    return dboutput

@app.route("/")
def index():
    session.pop('erabiltzailea', None)
    return render_template("root.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',error = None)
    elif request.method == 'POST':
        username = request.form['erabiltzailea']
        password = request.form['pasahitza']
        
        if dboutput.erabiltzailea_egiaztatu(username, password): #llama a la funcion de arriba q mira en la base de datos
            session['erabiltzailea'] = username #guarda el usuario en session que es como una memoria temporal del flask
            return redirect(url_for('control')) #manda al usuario a la siguiente pagina, en este caso dashboard
        else:
            return render_template('login.html',error = "Erabiltzaile edo pasahitz ezegokia")
        
@app.route('/sign-up', methods=['GET','POST'])
def erregistratu():
    if request.method == 'GET':
        return render_template('sign_up.html',error=None)
    elif request.method == 'POST':
        izena = request.form.get('izena')
        abizena = request.form.get('abizena')
        pasahitza = request.form.get('pasahitza')
        email = request.form.get('email')
        dokumentuak = request.form.get('dokumentuak')

        if dbinput.insert_Erabiltzaileak(izena, abizena, pasahitza, email, dokumentuak):
            session['erabiltzailea'] = izena
            return redirect(url_for('control'))
        else:
            return render_template('sign_up.html',error="Jadanik existitzen da erabiltzaile bat izen horrekin.")

@app.route("/control")
def control():
    page = mapPage(droneID)
    print(dboutput.get_Erabiltzaile_id(session['erabiltzailea']))
    return page.map(droneID)

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


@app.route("/map", methods=["GET", "POST"])
def callMap():
    print(droneID)
    page = mapPage(droneID)
    content = page.map(droneID)

    return content

@app.route('/get_coords', methods=['POST'])
def get_coords():
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']
    print(lat)
    print(lng)
    return jsonify({'lat': lat, 'lng': lng})
