import re
from datetime import *

from flask import *
from flask_mysqldb import MySQL

import env
# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

from controller.database_controller import *
from controller.insert_path import *
from controller.utils import *
from controller.modify_drone import *

from model.dronea import dronea

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

dboutput=output(mysql)
dbinput=input(mysql)

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
            session['erabiltzailea'] = dboutput.get_erab_full(username).erab_izen                   # Erabiltzailea "session" baten gordetzen du, flask-ek kudeatzen du
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
            session['erabiltzailea'] = dboutput.get_erab_full(izena).erab_izen
            return redirect(url_for('control'))
        else:
            print("Oh cock")
            return render_template('sign_up.html',error="Jadanik existitzen da erabiltzaile bat izen horrekin.")

@app.route("/control", methods=['GET','POST'])
def control():
    try:
        if request.method == 'GET':
            print("USERNAME EPIKOA:")
            print(session['erabiltzailea'])

            erab = dboutput.get_erab_full(session['erabiltzailea'])
            droneak=dboutput.get_erab_drone_list(erab)

            droneen_izenak = []
            for dronea in droneak:
                
                if(dronea.drone_jabea.erab_id != erab.erab_id):
                    droneen_izenak.append("{0}_{1}".format(dronea.drone_izen, dronea.drone_jabea.erab_izen))
                else:
                    droneen_izenak.append(dronea.drone_izen)

            header, body_html, script=mapInit.map_empty()
            return render_template("control.html", header=header, body_html=body_html, script=script, droneak=droneak)
        elif request.method == 'POST':
            droneReq=int(request.form.get('droneReq'))
            print("REQUESTED DRONE:",end="")
            print(droneReq)
            selected_drone = dboutput.get_drone_full(droneReq)
            ikusi=None

            erab = dboutput.get_erab_full(session['erabiltzailea'])
            droneak=dboutput.get_erab_drone_list(erab)
            droneen_izenak = []
            for drone in droneak:
                droneen_izenak.append(drone.drone_izen)
            
            droneID=selected_drone.drone_id
                    
            page = mapPage(dboutput,droneID)
            header, body_html, script=page.map()

            if erab.erab_id in selected_drone.drone_kontroladoreak:
                print(erab.erab_id)
                print(selected_drone.drone_kontroladoreak)
                ikusi=1
            else:
                ikusi=0
            return render_template("control.html", header=header, body_html=body_html, script=script, dronea=selected_drone.drone_izen, droneID=droneID, droneak=droneak, ikusi=ikusi)
    except KeyError as e:
        return redirect(url_for('index'))
    

@app.route("/insert_path/<droneIzen>", methods=['GET','POST'])
def insert_path(droneIzen):
    drone = dboutput.get_drone_full(droneIzen)
    return(insertPath.insertWaypoints(drone))


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
            erab = dboutput.get_erab_full(session['erabiltzailea'])
            print("IZENADRONE")
            print(izenaDrone)
            drone = dboutput.get_drone_full(izenaDrone)
            dbinput.insert_Partekatzeak(erab,drone,"Jabea")
            
            
            
            return redirect(url_for('control'))
    except KeyError as e:
        return redirect(url_for('index'))

@app.route("/modify_drone/<drone>", methods=['GET','POST'])
def modify_drone_page(drone):
    droneData = dboutput.get_drone_full(drone)
    return (modify_drone(droneData, dbinput, dboutput))
    
@app.route('/insert-sensor', methods=['GET','POST'])
def insert_sensor():
    if request.method == 'GET':
        return render_template('insert_sensor.html',error=None)
    elif request.method == 'POST':
        izenaSentsorea = request.form.get('izenaSentsorea')
        motaSentsorea = request.form.get('motaSentsorea')
        deskribapenaSentsorea = request.form.get('deskribapenaSentsorea')

        if dbinput.insert_Sentsoreak(izenaSentsorea, motaSentsorea, deskribapenaSentsorea):
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

    dbinput.insert_GPS_kokapena(content['robiotId'], content['lon'], content['lat'], content['alt'], content['hdg'], time_parsed, "DOW")
    waypoint = []
    waypoint = dboutput.get_next_waypoint(content['robiotId'])

    if len(waypoint) > 0:
        #print(getGPSDistance([content['lat'], content['lon']], [waypoint[0], waypoint[1]]))
        reply = {
            "gwid":gwid,
            "robiotId" : content['robiotId'],
            "wpLat" : waypoint[0],
            "wpLon" : waypoint[1],
            "wpAlt" : waypoint[2],
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

@app.route("/debug", methods=['GET', 'POST'])
def debug_show():
    erab = dboutput.get_erab_full(5)
    drone = dboutput.get_drone_full(4)
    return render_template("debugShowVar.html",var=dboutput.get_gps_full(drone))

# API FOR LIVE UPDATES
@app.route("/getLiveData", methods=['POST'])
def getLivePos():   
    data = request.get_json()
    droneID = data['droneID']

    drone = dboutput.get_drone_full(int(droneID))
    gpsData = dboutput.get_gps_full(drone)
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
