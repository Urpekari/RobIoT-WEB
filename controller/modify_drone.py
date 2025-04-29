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

from view.mapPage import *
from view.mapinit import *
from view.mapplan import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = env.mysql_host_ip
app.config['MYSQL_USER'] = env.mysql_username
app.config['MYSQL_PASSWORD'] = env.mysql_password
app.config['MYSQL_DB'] = env.mysql_db_name
app.secret_key = 'hackerdeminecraft'

def modifyDrone(drone):
    droneak,id=get_erab_drone_list(session['erabiltzailea'])

    for pos,dronea in enumerate(droneak):
        if dronea == drone:
            droneID=id[pos]
    jabe_id = dboutput.get_drone_jabe(droneID)
    jabe = dboutput.get_erab_izen(jabe_id)
    drone_info = dboutput.get_drone_info(droneID)
    partekatu_erab = dboutput.get_drone_erab(droneID)
    partekatuak = []
    for erab in partekatu_erab:
        if not erab[-1] == "Jabea":
            izen=dboutput.get_erab_izen(erab[1])
            partekatuak.append([izen,erab[-1]])
    sents_id = dboutput.get_drone_sentsoreak(droneID)
    sents_in = []
    for id in sents_id:
        sens_info = dboutput.get_sentsore_info(id[-1])
        sents_in.append(sens_info)

    if request.method == "GET":
        return render_template('modify_drone.html',drone=drone_info, jabe=jabe, partekatuak=partekatuak, sents_in=sents_in)
    
    elif request.method == "POST":
        bot = request.form.get('botoia')
        baimenak=[]
        error=None
        sentsoreak = []
        if bot == '2':
            sentsore_guztiak = dboutput.get_info(tables.Sentsoreak)
            for sents in sentsore_guztiak:
                if sents not in sents_in:
                    sentsoreak.append(sents)
        elif bot == '3':
            baimen_info=dboutput.get_info(tables.Baimenak)
            for row in baimen_info:
                for baimen in row:
                    if baimen not in ["Admin","Jabea"]:
                        baimenak.append(baimen)
        elif bot == '4':
            izena = request.form.get('izen')
            mota = request.form.get('mota')
            deskribapena = request.form.get('deskribapena')
            dbinput.update_Droneak(izena,mota,deskribapena,droneID)
            drone_info = dboutput.get_drone_info(droneID)
        elif bot == '5':
            sentsoreak = dboutput.get_info(tables.Sentsoreak)
            for element in sentsoreak:
                sens = request.form.get(str(element[0]))
                if sens:
                    dbinput.insert_Drone_Sentsore(None,droneID,int(sens))
            sents_id = dboutput.get_drone_sentsoreak(droneID)
            sents_in = []
            for id in sents_id:
                sens_info = dboutput.get_sentsore_info(id[-1])
                sents_in.append(sens_info)
        elif bot == '6':
            partekatu_erab = request.form.get('partekatu_erab')
            baimena = request.form.get('baimena')
            id_erab=dboutput.get_erab_id(partekatu_erab)
            if id_erab:
                dbinput.insert_Partekatzeak(id_erab,droneID,baimena)
            else:
                error="Ez da erabiltzaile hori existitzen"
            partekatu_erab = dboutput.get_drone_erab(droneID)
            partekatuak = []
            for erab in partekatu_erab:
                if not erab[-1] == "Jabea":
                    izen=dboutput.get_erab_izen(erab[1])
                    partekatuak.append([izen,erab[-1]])
        return render_template('modify_drone.html',drone=drone_info, jabe=jabe, aukera=bot, baimenak=baimenak, error=error, sentsoreak=sentsoreak, partekatuak=partekatuak, sents_in=sents_in)
