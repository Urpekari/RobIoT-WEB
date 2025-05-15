import re
from datetime import *

from flask import *
from flask_mysqldb import MySQL

import env
# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

from controller.database_controller import database_controller
from view.insert_path import *
from controller.utils import *
from view.modify_drone import *

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
            ikusi = 1
            ikus_baimen = 1
            droneak = database.lortu_erabiltzailearen_droneak(session['erabiltzailea'])
            drone_izen_jabe = ""
            for dronea in droneak:
                if dronea.partekatze_drone.drone_id == selected_drone.drone_id:
                    drone_izen_jabe = str(selected_drone.drone_izen) + "_" + dronea.partekatze_erab.erab_izen
                    if dronea.partekatze_baimen == "Ikusi":
                        ikus_baimen = 0

            page = mapPage(database,droneReq)
            header, body_html, script=page.map()
            return render_template("control.html", header=header, body_html=body_html, script=script, dronea=selected_drone, droneak=droneak, drone_izen_jabe=drone_izen_jabe, ikusi=ikusi, ikus_baimen=ikus_baimen)
    
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
    return (modify_drone(drone_id, database, drone, session['erabiltzailea']))  # <----------- FALTA!!!!!!!!!!!!!!!!!

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
    try:
        gwid_interp = int(gwid)
        
        content = request.get_json()

        #print("CONTENT")
        #print(content)

        date = datetime.now()
        #print(date)
        time_parsed = date #.strftime("%y-%m-%d %H:%M:%S.%f")

        database.sartu_momentuko_kokapena(content['robiotId'], content['lon'], content['lat'], content['alt'], content['hdg'], time_parsed)
        
        waypoint = []
        waypoint = database.lortu_hurrengo_jauzia(content['robiotId'])
        distance_to_wp = getGPSDistance([float(content['lat']), float(content['lon'])], [waypoint.gps_lat, waypoint.gps_lng])
        print(distance_to_wp, end='')
        print("m-ko distantzia")
        if(distance_to_wp<100):
            database.eguneratu_heldutako_waypoint(waypoint.gps_id)
            waypoint = database.lortu_hurrengo_jauzia(content['robiotId'])

        #print(waypoint.get_gps_coords())

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
    except:
        
       return Response("BAD REQUEST", status=400)

@app.route('/get_coords', methods=['POST'])
def get_coords():
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']
    #print(lat)
    #print(lng)
    return jsonify({'lat': lat, 'lng': lng})

@app.route("/debug", methods=['GET', 'POST']) #<---------------------- Creo que son pruebas (borrar)
def debug_show():


    try:
        # INT espero duen funtzio baten String, int, existitzen ez den drone bat eta char sartzen.
        # Hau API-ko funtzioa denez, garrantzitsua da gwid-ak ez inbentatu izana
        gw_insert_emaitzak = [gw_insert("Patata"), gw_insert('E'), gw_insert(None), gw_insert(1), gw_insert(2)]
        if(None in gw_insert_emaitzak):
            gw_emaitza = "FAIL"
        else:
            gw_emaitza = "PASS"
    except:
        gw_emaitza = "FAIL"

    try:
        # INT Espero duen funtzio baten String, int, none eta objektu bat sartzen.
        lortu_drone_info_osoa_emaitzak = [database.lortu_drone_info_osoa("Patata"), database.lortu_drone_info_osoa(1), database.lortu_drone_info_osoa(None), database.lortu_drone_info_osoa(database.lortu_drone_GPS_informazioa(1)), database.lortu_drone_info_osoa(5000)]
        if(None in lortu_drone_info_osoa_emaitzak):
            drone_emaitza = "FAIL"
        else:
            drone_emaitza = "PASS"
    except:
        drone_emaitza = "FAIL"

    try:
        # INT Espero duen funtzio baten String, int, none eta objektu bat sartzen.
        lortu_drone_GPS_informazioa_emaitzak = [database.lortu_drone_GPS_informazioa("Patata"), database.lortu_drone_GPS_informazioa(1), database.lortu_drone_GPS_informazioa(None), database.lortu_drone_GPS_informazioa(database.lortu_drone_info_osoa(1))]
        if(None in lortu_drone_GPS_informazioa_emaitzak):
            gps_emaitza = "FAIL"
        else:
            gps_emaitza = "PASS"
    except:
        gps_emaitza = "FAIL"
    

    return render_template("debugShowVar.html",var=[["gw_insert", gw_emaitza], ["lortu_drone_info_osoa", drone_emaitza], ["lortu_drone_GPS_informazioa", gps_emaitza]])


# API FOR LIVE UPDATES
@app.route("/getLiveData", methods=['POST'])
def getLivePos():   
    data = request.get_json()
    droneID = data['droneID']

    gpsData = database.lortu_drone_GPS_informazioa(int(droneID))
    dronePos = __filterPositionLogs(gpsData)
    futureWPs = __filterWaypoints(gpsData, False)

    nextWP = None
    goalWP = None

    if not len(futureWPs) == 0:
        nextWP = futureWPs[0]
        goalWP = futureWPs[-1]

    fullSimpleRemainingPath = __filterSimplePath(futureWPs)
    
    if not len(dronePos) == 0:
        fullSimpleRemainingPath.insert(0, dronePos[-1].get_gps_coords())

    # TODO:deltaT zehatzagoak lortu... behintzat azpiegitura hor dugu!
    
    if nextWP:
        deltapos = getGPSDistance(compareCoords=nextWP.get_gps_coords(), currentCoords=dronePos[-1].get_gps_coords())
        deltaT = (dronePos[-1].get_gps_timestamp() - dronePos[-2].get_gps_timestamp()).total_seconds()

    return jsonify({
        
        'GPSPos':{
            'lat': dronePos[-1].get_gps_lat() if dronePos else "NAN",
            'lng': dronePos[-1].get_gps_lng() if dronePos else "NAN",
            'cur': dronePos[-1].get_gps_timestamp() if dronePos else "NAN"
        },
        'NextWaypoint':{
            'lat': nextWP.get_gps_lat() if nextWP else "NAN",
            'lng': nextWP.get_gps_lng()  if nextWP else "NAN",
            'eta': datetime.now() + timedelta(seconds=getEta(deltapos, deltapos/deltaT)) if nextWP else "NAN",
        },

        'Destination':{
            'lat': goalWP.get_gps_lat() if goalWP else "NAN",
            'lng': goalWP.get_gps_lng() if goalWP else "NAN",
            'eta': datetime.now() + timedelta(seconds = getEta(distance=getFullPathDistance(gpsPathWPs=fullSimpleRemainingPath), speed=(deltapos/deltaT))) if goalWP else "NAN"
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
