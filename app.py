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
    try:
        if request.method == 'GET':
            droneak,_=get_erab_drone_list(session['erabiltzailea'])
            header, body_html, script=mapInit.map_empty()
            return render_template("control.html", header=header, body_html=body_html, script=script, droneak=droneak)
        elif request.method == 'POST':
            drone_izena=request.form.get('drone_izena')
            ikusi=None
            droneak,id=get_erab_drone_list(session['erabiltzailea'])
            for pos,drone in enumerate(droneak):
                if drone == drone_izena:
                    droneID=id[pos]
            page = mapPage(droneID)
            header, body_html, script=page.map()
            if not drone_izena[-6:] == "_ikusi":
                ikusi=1
            return render_template("control.html", header=header, body_html=body_html, script=script, dronea=drone_izena, droneak=droneak, ikusi=ikusi)
    except KeyError as e:
        return redirect(url_for('index'))
    
def get_erab_drone_list(erab):
    erab_id=dboutput.get_erab_id(erab)
    id_drone,baimen=dboutput.get_erab_droneak(erab_id)
    droneak=[]
    for pos,id in enumerate(id_drone):
        drone=dboutput.get_drone_info(id)
        jabe_id=dboutput.get_drone_jabe(id)
        jabe_izen=dboutput.get_erab_izen(jabe_id)
        if not jabe_izen==erab:
            drone=drone+"_"+jabe_izen
            if baimen[pos] == "Kontrolatu":
                drone=drone+"_kontrolatu"
            elif baimen[pos] == "Ikusi":
                drone=drone+"_ikusi"
        droneak.append(drone)
    return droneak,id_drone

@app.route("/insert_path/<drone>", methods=['GET','POST'])
def insert_path(drone):
    try:
        if request.method == 'GET':
            header, body_html, script=mapInit.map_empty()
            return render_template("insert_path.html", header=header, body_html=body_html, script=script, dronea=drone)
        elif request.method == 'POST':
            bot=request.form.get('botoia')
            lat=""
            long=""
            list=[]
            error = None
            liststr=request.form.get('list')
            if liststr:
                listtmp = re.findall('\[(.*?)\]',liststr)
                for coord in listtmp:
                    coord = re.findall('\'(.*?)\'',coord)
                    list.append(coord)
                if list[0]==[]:
                    list=list[1:]
            
            if bot == '1': 
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
                root.destroy()
                return render_template("insert_path.html", header=header, body_html=body_html, script=script, lat=lat, long=long, list=list, error=error, dronea=drone)

            elif bot == '2':
                latin = request.form.get('lat')
                longin = request.form.get('long')
                coords = [latin,longin]
                list.append(coords)
                if list[0]==[]:
                    list=list[1:]
            
                if list:
                    header, body_html, script=mapInit.map_with_pointers(list)
                else:
                    header, body_html, script=mapInit.map_empty()
                return render_template("insert_path.html", header=header, body_html=body_html, script=script, lat=lat, long=long, list=list, error=error, dronea=drone)
            
            elif bot == '3':
                droneak,id=get_erab_drone_list(session['erabiltzailea'])
                for pos,dronea in enumerate(droneak):
                    if dronea == drone:
                        droneID=id[pos]
                for coords in list:
                    dbinput.insert_GPS_kokapena(droneID,coords[1],coords[0],None,datetime.now(),"UPF")
                
                return redirect(url_for('control'))
    except KeyError as e:
        return redirect(url_for('index'))

@app.route('/insert-drone', methods=['GET','POST'])
def drone_erregistratu():
    try:
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
    except KeyError as e:
        return redirect(url_for('index'))

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

#@app.route("/database")
#def database_show():
#    return render_template(
#        "database.html",
#        header=tables.Droneak_header,
#        items=dboutput.get_info(tables.Droneak)
#    )

#@app.route("/database/dowload")
#def download_csv():
#    csv = dboutput.create_csv(tables.Droneak)
#    return Response(
#        csv,
#        mimetype="text/csv",
#        headers={"Content-disposition":
#                 "attachment; filename=Erabiltzaileak.csv"})

#@app.route("/database/insert",methods=['POST'])
#def in_drone():
#    info=(request.form["izena"],request.form["mota"],request.form["deskribapena"])
#    dbinput.insert_Droneak(info)
#    return redirect(url_for("database_show"))
