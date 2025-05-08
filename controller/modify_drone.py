import re
from datetime import *
import numpy as np

from flask import *
from flask_mysqldb import MySQL

import env
# env.py fitxategia EZ DA GITHUBERA IGOKO.
# .gitignore fitxategi baten bera ekidituko dugu!

# Hau agian view-ean egon behar du

from controller.database_controller import *
from controller.insert_path import *
from controller.utils import *

from app import *

from view.mapPage import *
from view.mapinit import *
from view.mapplan import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = env.mysql_host_ip
app.config['MYSQL_USER'] = env.mysql_username
app.config['MYSQL_PASSWORD'] = env.mysql_password
app.config['MYSQL_DB'] = env.mysql_db_name
app.secret_key = 'hackerdeminecraft'

def modify_drone(drone, dbinput, dboutput):
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    #print(app.session)
    #session = app.session['erabiltzailea']
    # droneak,id=get_erab_drone_list(session)

    # for pos,dronea in enumerate(droneak):
    #     if dronea == drone:
    #         drone.drone_id=id[pos]
    jabe = dboutput.get_drone_jabe(drone.drone_id)
    print("DRONE HONEN:", end="")
    print(drone.drone_id, end="")
    print(" JABEA HAU DA:", end="")
    print(jabe.erab_id)

    partekatu_erab = []
    for kontrol in drone.drone_kontroladoreak:
        partekatu_erab.append(kontrol)
        
    for ikus in drone.drone_ikusleak:
        partekatu_erab.append(ikus)

    print(partekatu_erab)
    partekatuak = []
    for erabId in partekatu_erab:
            partekatuak = (dboutput.get_partekatze_full_droneArabera(drone))
    sents_in = drone.drone_sentsoreak

    if request.method == "GET":
        return render_template('modify_drone.html',drone=[drone.drone_id, drone.drone_izen, drone.drone_mota, drone.drone_desk], jabe=jabe.erab_izen, partekatuak=partekatuak, sents_in=sents_in)
    
    elif request.method == "POST":
        bot = request.form.get('botoia')
        baimenak=[]
        error=None
        sentsoreak = []

        # "Sentsore gehitu" botoia
        if bot == '2':
            sentsoreak = dboutput.get_sentsore_guztiak()

        # "Partekatu" botoia
        elif bot == '3':
            baimen_info=dboutput.get_baimen_posible_zerrenda()
            for row in baimen_info:
                for baimen in row:
                    if baimen not in ["Admin","Jabea"]:
                        baimenak.append(baimen)

        
        elif bot == '4':
            izena = request.form.get('izen')
            mota = request.form.get('mota')
            deskribapena = request.form.get('deskribapena')
            dbinput.update_Droneak(izena,mota,deskribapena,drone.drone_id)

        # Sentsore berriak sartzeko "Sartu" botoia
        elif bot == '5':
            sens = request.form.getlist("sentsorea")
            print("SENS: SENS:")
            print(sens)

            for sentsore in sens:
                dbinput.insert_Drone_Sentsore(None,drone.drone_id, int(sentsore))
            sents_in = drone.drone_sentsoreak
        
        elif bot == '6':
            partekatu_erab = request.form.get('partekatu_erab')
            baimena = request.form.get('baimena')
            erab=dboutput.get_erab_full(partekatu_erab)
            if erab:
                dbinput.insert_Partekatzeak(erab,drone,baimena)
                partekatuak = (dboutput.get_partekatze_full_droneArabera(drone))
            else:
                error="Ez da erabiltzaile hori existitzen"
            
        drone = dboutput.get_drone_full(drone.drone_id)

    return render_template('modify_drone.html',drone=[drone.drone_id, drone.drone_izen, drone.drone_mota, drone.drone_desk], jabe=jabe.erab_izen, aukera=bot, baimenak=baimenak, error=error, sentsoreak=sentsoreak, partekatuak=partekatuak, sents_in=drone.drone_sentsoreak)