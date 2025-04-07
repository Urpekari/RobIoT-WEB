import re
from datetime import datetime

from flask import *
from flask_mysqldb import MySQL

import env
from view.droneControlPage import *
from controller.database_controller import *

import tkinter as tk


app = Flask(__name__)

#TODO: LORTU DRONEID DINAMIKOKI

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
        
        if dboutput.erabiltzailea_egiaztatu(username, password):    # Goiko datu-base funtzioa deitzen du
            session['erabiltzailea'] = username                     # Erabiltzailea "session" baten gordetzen du, flask-ek kudeatzen du
            return redirect(url_for('control'))                     # Hurrengo orrira bidaltzen du erabiltzailea
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

@app.route("/control", methods=['GET','POST'])
def control():
    if request.method == 'GET':
        erab_id=dboutput.get_erab_id(session['erabiltzailea'])
        id_drone=dboutput.get_erab_droneak(erab_id)
        droneak=[]
        for id in id_drone:
            drone=dboutput.get_drone_info(id)
            droneak.append(drone)
        header, body_html, script=mapInit.map_empty()
        return render_template("control.html", header=header, body_html=body_html, script=script, droneak=droneak)
    elif request.method == 'POST':
        drone_izena=request.form.get('drone_izena')
        erab_id=dboutput.get_erab_id(session['erabiltzailea'])
        id_drone=dboutput.get_erab_droneak(erab_id)
        droneak=[]
        for id in id_drone:
            drone=dboutput.get_drone_info(id)
            if drone == drone_izena:
                droneID=id
            droneak.append(drone)
        page = mapPage(droneID)
        header, body_html, script=page.map()
        return render_template("control.html", header=header, body_html=body_html, script=script, dronea=drone_izena, droneak=droneak)
    

@app.route("/insert_path", methods=['GET','POST'])
def froga():
    if request.method == 'GET':
        header, body_html, script=mapInit.map_empty()
        return render_template("insert_path.html", header=header, body_html=body_html, script=script)
    elif request.method == 'POST':

        bot=request.form.get('botoia')
        lat=""
        long=""
        list=[]
        error = None
        if bot == '2':
            liststr = request.form.get('list')
            latin = request.form.get('lat')
            longin = request.form.get('long')
            coords = [latin,longin]
            if liststr:
                listtmp = re.findall('\[(.*?)\]',liststr)
                for coord in listtmp:
                    coord = re.findall('\'(.*?)\'',coord)
                    list.append(coord)
            list.append(coords)
            if list[0]==[]:
                list=list[1:]

        elif bot == '1':
            liststr=request.form.get('list')
            if liststr:
                listtmp = re.findall('\[(.*?)\]',liststr)
                for coord in listtmp:
                    coord = re.findall('\'(.*?)\'',coord)
                    list.append(coord)
                if list[0]==[]:
                    list=list[1:]
            root=tk.Tk()
            clipboard_content = root.clipboard_get()
            lines = clipboard_content.split(',')
            if len(lines)<2:
                error="Ez dira koordenatuak ondo kopiatu"
            else:
                lat=lines[0]
                long=lines[1]
        
        if list:
            header, body_html, script=mapInit.map_with_pointers(list)
        else:
            header, body_html, script=mapInit.map_empty()

        return render_template("insert_path.html", header=header, body_html=body_html, script=script, lat=lat, long=long, list=list, error=error)

@app.route('/insert_drone', methods=['GET','POST'])
def erregistratu2():
    if request.method == 'GET':
        return render_template('insert_drone.html')
    elif request.method == 'POST':
        izenaDrone = request.form.get('izenaDrone')
        mota = request.form.get('mota')
        deskribapena = request.form.get('deskribapena')

        dbinput.insert_Droneak(izenaDrone, mota, deskribapena)
        erab_id=dboutput.get_erab_id(session['erabiltzailea'])
        drone_id=dboutput.get_drone_id(izenaDrone, mota, deskribapena)
        dbinput.insert_Partekatzeak(erab_id,drone_id,"Jabea")
        return redirect(url_for('control'))

@app.route("/gwInsert/<gwid>",methods=['POST'])
def gw_insert(gwid):
    content = request.get_json()

    date = datetime.now()
    print(date)
    time_parsed = date #.strftime("%y-%m-%d %H:%M:%S.%f")

    dbinput.insert_GPS_kokapena(content['robiotId'], content['lon'], content['lat'], content['alt'], time_parsed, "DOW")
    waypoints = []
    waypoints = dboutput.get_next_waypoint(content['robiotId'])
    
    print(waypoints)

    reply = {

        "gwid":gwid,
        "robiotId" : content['robiotId'],
        "wpLat":waypoints[0],
        "wpLon" : waypoints[1],
        "wpAlt" : waypoints[2],
    }

    return(reply)

@app.route('/get_coords', methods=['POST'])
def get_coords():
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']
    print(lat)
    print(lng)
    return jsonify({'lat': lat, 'lng': lng})
