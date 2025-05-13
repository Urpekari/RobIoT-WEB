import re
from datetime import *

from flask import *
from flask_mysqldb import MySQL

import env
# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

from controller.database_controller import database_controller
from controller.insert_path import *
from controller.utils import *
from controller.modify_drone import *

from model import *

from view.mapPage import *
from view.mapinit import *
from view.mapplan import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = env.mysql_host_ip
app.config['MYSQL_USER'] = env.mysql_username
app.config['MYSQL_PASSWORD'] = env.mysql_password
app.config['MYSQL_DB'] = env.mysql_db_name
app.secret_key = 'hackerdeminecraft'

mysql=MySQL(app)

database = database_controller(mysql)

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
        erab,erabExist = database.erabiltzailea_egiaztatu(username, password)
        if erabExist:
            session['erabiltzailea'] = erab.erab_id
            return redirect(url_for('control'))
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

        if database.sartu_erabiltzaile_berria(izena, abizena, pasahitza, email, dokumentuak):
            session['erabiltzailea'] = database.lortu_erabiltzailea(izena).erab_id
            return redirect(url_for('control'))
        else:
            return render_template('sign_up.html',error="Jadanik existitzen da erabiltzaile bat izen horrekin.")

@app.route("/control", methods=['GET','POST'])
def control():
    try:
        if request.method == 'GET':

            droneak = database.lortu_erabiltzailearen_droneak(session['erabiltzailea'])
            header, body_html, script=mapInit.map_empty()
            return render_template("control.html", header=header, body_html=body_html, script=script, droneak=droneak)
        
        elif request.method == 'POST':
            droneReq = int(request.form.get('droneReq'))
            selected_drone = database.lortu_dronea(droneReq)
            ikusi = 0
            droneak = database.lortu_erabiltzailearen_droneak(session['erabiltzailea'])
            drone_izen_jabe = ""
            for dronea in droneak:
                if dronea.partekatze_drone.drone_id == selected_drone.drone_id:
                    drone_izen_jabe = str(selected_drone.drone_izen) + "_" + dronea.partekatze_erab.erab_izen
                    if dronea.partekatze_baimen == "Ikusi":
                        ikusi = 0

                    else:
                        ikusi = 1

            page = mapPage(database,droneReq)
            header, body_html, script=page.map()
            return render_template("control.html", header=header, body_html=body_html, script=script, dronea=selected_drone, droneak=droneak, drone_izen_jabe=drone_izen_jabe, ikusi=ikusi)
    
    except KeyError as e:
        return redirect(url_for('index'))
    

@app.route("/insert_path/<drone>", methods=['GET','POST'])
def insert_path(drone):
    drone_info = drone.split('_')
    drone_izen = drone_info[0]
    drone_jabe = drone_info[1]
    droneak = database.lortu_erabiltzailearen_droneak(session['erabiltzailea'])
    selected_drone = None
    for dron in droneak:
        if dron.partekatze_drone.drone_izen == drone_izen and dron.partekatze_erab.erab_izen == drone_jabe:
            selected_drone = dron.partekatze_drone

    return(insertPath.insertWaypoints(selected_drone, drone)) # <----------- FALTA!!!!!!!!!!!!!!!!!


@app.route('/insert-drone', methods=['GET','POST'])
def drone_erregistratu():
    try:
        if request.method == 'GET':
            return render_template('insert_drone.html')
        
        elif request.method == 'POST':
            izenaDrone = request.form.get('izenaDrone')
            mota = request.form.get('mota')
            deskribapena = request.form.get('deskribapena')
            database.sartu_drone_berria(izenaDrone, mota, deskribapena, session['erabiltzailea'])
            return redirect(url_for('control'))
        
    except KeyError as e:
        return redirect(url_for('index'))

@app.route("/modify_drone/<drone>", methods=['GET','POST'])
def modify_drone_page(drone):
    drone_info = drone.split('_')
    drone_izen = drone_info[0]
    drone_jabe = drone_info[1]
    droneak = database.lortu_erabiltzailearen_droneak(session['erabiltzailea'])
    drone_id = 0
    for dron in droneak:
        if dron.partekatze_drone.drone_izen == drone_izen and dron.partekatze_erab.erab_izen == drone_jabe:
            drone_id = dron.partekatze_drone.drone_id
    return (modify_drone(drone_id, database, drone))  # <----------- FALTA!!!!!!!!!!!!!!!!!

@app.route('/izen-aldaketa/<drone>/<izen_berri>', methods=['GET'])
def izen_aldaketa(drone,izen_berri):
    drone_info = drone.split('_')
    drone_jabe = drone_info[1]
    drone_info_berri = izen_berri + "_" + drone_jabe
    return redirect(url_for('modify_drone_page',drone=drone_info_berri))

@app.route('/insert-sensor', methods=['GET','POST'])
def insert_sensor():
    if request.method == 'GET':
        return render_template('insert_sensor.html',error=None)
    
    elif request.method == 'POST':
        izenaSentsorea = request.form.get('izenaSentsorea')
        motaSentsorea = request.form.get('motaSentsorea')
        deskribapenaSentsorea = request.form.get('deskribapenaSentsorea')

        if database.sartu_sentsore_berria(izenaSentsorea, motaSentsorea, deskribapenaSentsorea):
            return redirect(url_for('control'))
        
        else:
            return render_template('insert_sensor.html',error="Jadanik existitzen da sentsore bat izen horrekin.")

@app.route("/gwInsert/<gwid>",methods=['POST'])
def gw_insert(gwid):
    content = request.get_json()

    print("CONTENT")
    print(content)

    date = datetime.now()
    print(date)
    time_parsed = date #.strftime("%y-%m-%d %H:%M:%S.%f")

    database.sartu_momentuko_kokapena(content['robiotId'], content['lon'], content['lat'], content['alt'], content['hdg'], time_parsed)
    waypoint = []
    waypoint = database.lortu_hurrengo_jauzia(content['robiotId'])

    if waypoint:
        #print(getGPSDistance([content['lat'], content['lon']], [waypoint[0], waypoint[1]]))
        reply = {
            "gwid":gwid,
            "robiotId" : content['robiotId'],
            "wpLat" : waypoint.gps_lat,
            "wpLon" : waypoint.gps_lng,
            "wpAlt" : waypoint.gps_alt,
        }
    else:
        reply = {
            "gwid":gwid,
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

@app.route("/debug", methods=['GET', 'POST']) #<---------------------- Creo que son pruebas (borrar)
def debug_show():
    return render_template("debugShowVar.html",var=database.lortu_hurrengo_jauzia(2))

# API FOR LIVE UPDATES
@app.route("/getLiveData", methods=['POST'])
def getLivePos():   
    data = request.get_json()
    droneID = data['droneID']

    gpsData = database.lortu_drone_GPS_informazioa(int(droneID))
    dronePos = __filterPositionLogs(gpsData)
    futureWPs = __filterWaypoints(gpsData, False)

    nextWP = futureWPs[0]
    goalWP = futureWPs[-1]

    fullSimpleRemainingPath = __filterSimplePath(futureWPs)
    fullSimpleRemainingPath.insert(0, dronePos[-1].get_gps_coords())

    # TODO:deltaT zehatzagoak lortu... behintzat azpiegitura hor dugu!
    
    deltapos = getGPSDistance(compareCoords=nextWP.get_gps_coords(), currentCoords=dronePos[-1].get_gps_coords())
    deltaT = (dronePos[-1].get_gps_timestamp() - dronePos[-2].get_gps_timestamp()).total_seconds()

    return jsonify({
        
        'GPSPos':{
            'lat': dronePos[-1].get_gps_lat(),
            'lng': dronePos[-1].get_gps_lng(),
            'cur': dronePos[-1].get_gps_timestamp()
        },
        'NextWaypoint':{
            'lat': nextWP.get_gps_lat(),
            'lng': nextWP.get_gps_lng(),
            'eta': datetime.now() + timedelta(seconds=getEta(deltapos, deltapos/deltaT))
        },

        'Destination':{
            'lat': goalWP.get_gps_lat(),
            'lng': goalWP.get_gps_lng(),
            'eta': datetime.now() + timedelta(seconds = getEta(distance=getFullPathDistance(gpsPathWPs=fullSimpleRemainingPath), speed=(deltapos/deltaT)))
        },

        })

## PROBAK EGITEKO ETA MISZELANEOAK ========================================================
@app.route("/database", methods=['GET','POST'])
def database_show():
    a1=request.form.get('a1')
    a2=request.form.get('a2')
    print(a1)
    print(a2)
    return render_template(
        "database.html",
    )

## HEMENDIK KENDU BEHARREKOAK ==============================================================
## HAUEK EZ DIRA OBJEKTUETAN JOATEKOAK!! BEGIRATU MAPPLAN!! ================================

# TODO: CONTROLLER-EAN SARTU
# GPS balio guztien artean waypoint-ak soilik hartzeko
def __filterWaypoints(rawGpsData:list, isPastWP:bool):
    waypoints = []
    for gpsPoint in rawGpsData:
        if gpsPoint.gps_way == True and gpsPoint.gps_past == isPastWP:
            waypoints.append(gpsPoint)
    return waypoints

# TODO: CONTROLLER-EAN SARTU
# GPS balioetatik koordenatuak lortzeko, zerrenda luze baten
def __filterSimplePath(rawGpsData):
    waypoints = []
    for gpsPoint in rawGpsData:
        waypoints.append(gpsPoint.get_gps_coords())
    return waypoints

# TODO: CONTROLLER-EAN SARTU
# GPS balio guztien artean dronearen benetako posizioak soilik hartzeko
def __filterPositionLogs(rawGpsData):
    posLog = []
    for gpsPoint in rawGpsData:
        if gpsPoint.gps_way == False:
            posLog.append(gpsPoint)
    return posLog

#@app.route("/database/dowload")
#def download_csv():
#    csv = database.create_csv(tables.Droneak)
#    return Response(
#        csv,
#        mimetype="text/csv",
#        headers={"Content-disposition":
#                 "attachment; filename=Erabiltzaileak.csv"})

#@app.route("/database/insert",methods=['POST'])
#def in_drone():
#    info=(request.form["izena"],request.form["mota"],request.form["deskribapena"])
#    database.__insert_Droneak(info)
#    return redirect(url_for("database_show"))
