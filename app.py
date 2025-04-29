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
            print("USERNAME EPIKOA:")
            print(session['erabiltzailea'])
            droneak,_=dboutput.get_erab_drone_list(session['erabiltzailea'])
            header, body_html, script=mapInit.map_empty()
            return render_template("control.html", header=header, body_html=body_html, script=script, droneak=droneak)
        elif request.method == 'POST':
            drone_izena=request.form.get('drone_izena')
            ikusi=None
            droneak,id=dboutput.get_erab_drone_list(session['erabiltzailea'])
            for pos,drone in enumerate(droneak):
                if drone == drone_izena:
                    droneID=id[pos]
            page = mapPage(dboutput,droneID)
            header, body_html, script=page.map()
            if not drone_izena[-6:] == "_ikusi":
                ikusi=1
            return render_template("control.html", header=header, body_html=body_html, script=script, dronea=drone_izena, droneID=droneID, droneak=droneak, ikusi=ikusi)
    except KeyError as e:
        return redirect(url_for('index'))
    


@app.route("/insert_path/<drone>", methods=['GET','POST'])
def insert_path(drone):

    droneak,id=dboutput.get_erab_drone_list(session['erabiltzailea'])

    for pos,dronea in enumerate(droneak):
        if dronea == drone:
            droneID=id[pos]

    return(insertPath.insertWaypoints(drone, droneID))

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

@app.route("/modify_drone/<drone>", methods=['GET','POST'])
def modify_drone_page(drone):
    return (modify_drone.modify_drone(drone))
    
@app.route('/insert_sensor', methods=['GET','POST'])
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
        print(getGPSDistance([content['lat'], content['lon']], [waypoint[0], waypoint[1]]))
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
    return render_template("debugShowVar.html",var=dboutput.get_erab_full(1).erab_email)

@app.route("/database", methods=['GET','POST'])
def database_show():
    a1=request.form.get('a1')
    a2=request.form.get('a2')
    print(a1)
    print(a2)
    return render_template(
        "database.html",
        header=tables.Droneak_header,
        items=dboutput.get_info(tables.Droneak)
    )

# API FOR LIVE UPDATES
@app.route("/getLiveData", methods=['POST'])
def getLivePos():   
    data = request.get_json()
    droneID = data['droneID']
    #print(droneID)
    dronePos = dboutput.getRealLocations(droneID)[-1]
    dronePosTimes = dboutput.get_timestamps(droneID, "DOW")
    futureWPs = dboutput.get_waypoint_future(droneID)
    nextWP = futureWPs[0]
    goalWP = dboutput.get_waypoint_future(droneID)[-1]
    futureWPs.insert(0, [dronePos[0], dronePos[1]])

    # TODO:deltaT zehatzagoak lortu... behintzat azpiegitura hor dugu!
    
    deltapos = getGPSDistance(compareCoords=[nextWP[0], nextWP[1]], currentCoords=[dronePos[0], dronePos[1]])
    deltaT = (dronePosTimes[-1][0] - dronePosTimes[-2][0]).total_seconds()

    return jsonify({
        
        'GPSPos':{
            'lat': dronePos[0],
            'lng': dronePos[1]
        },
        'NextWaypoint':{
            'lat': nextWP[0],
            'lng': nextWP[1],
            'eta': datetime.now() + timedelta(seconds=getEta(deltapos, deltapos/deltaT))
        },

        'Destination':{
            'lat': goalWP[0],
            'lng': goalWP[1],
            'eta': datetime.now() + timedelta(seconds = getEta(distance=getFullPathDistance(gpsPathWPs=futureWPs), speed=(deltapos/deltaT)))
        },

        })


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
