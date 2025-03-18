import re
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template, Response, session, jsonify
from flask_mysqldb import MySQL
import database

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'RobIoT'
app.config['MYSQL_PASSWORD'] = 'RobIoT'
app.config['MYSQL_DB'] = 'robiot'

mysql = MySQL(app)

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
    
    if database.erabiltzailea_egiaztatu(mysql,username, password): #llama a la funcion de arriba q mira en la base de datos
        #session['usuario'] = username #guarda el usuario en session que es como una memoria temporal del flask
        return redirect(url_for('database_show')) #manda al usuario a la siguiente pagina, en este caso dashboard
    else:
        return "Usuario o contraseña incorrectos", 401 #401 es el código de estado HTTP para "No autorizado".

@app.route("/database")
def database_show():
    return render_template(
        "database.html",
        header=database.Droneak_header,
        items=database.get_info(mysql,database.Droneak)
    )

@app.route("/database/dowload")
def download_csv():
    csv = database.create_csv(mysql,database.Droneak)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Erabiltzaileak.csv"})

@app.route("/database/insert",methods=['POST'])
def in_drone():
    info=(request.form["izena"],request.form["mota"],request.form["deskribapena"])
    database.insert_Droneak(mysql,info)
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

@app.route('/erregistratu', methods=['POST'])
def erregistratu():
    izena = request.form.get('izena')
    abizena = request.form.get('abizena')
    pasahitza = request.form.get('pasahitza')
    email = request.form.get('email')
    dokumentuak = request.form.get('dokumentuak')

    if izena and abizena and pasahitza and email and dokumentuak:
        if datuak_sartu(izena, abizena, pasahitza, email, dokumentuak):
            return jsonify({"mensaje": "Zuzen erregistratu zara!"}), 201
        else:
            return jsonify({"error": "Arazoa erregistratzerakoan"}), 500
    return jsonify({"error": "Beharrezkoak diren datu guztiak sartu behar dituzu. (izena eta pasahitza)"}), 400

if __name__ == '__main__':#esto nose para que se hace
    app.run(debug=True)


def datuak_sartu(izena, abizena, pasahitza, email, dokumentuak):
    try:
        cursor = mysql.connection.cursor()
        query = "INSERT INTO registros (izena, abizena, pasahitza, email, dokumentuak) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (izena, abizena, pasahitza, email, dokumentuak))
        mysql.connection.commit()
        return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        cursor.close()
