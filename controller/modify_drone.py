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

def modify_drone(drone_id, database, drone_izen_jabe):
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    #print(app.session)
    #session = app.session['erabiltzailea']
    # droneak,id=get_erab_drone_list(session)

    # for pos,dronea in enumerate(droneak):
    #     if dronea == drone:
    #         drone.drone_id=id[pos]
    drone_info = database.lortu_drone_info_osoa(drone_id)
    

    if request.method == "GET":
        return render_template('modify_drone.html', drone_info=drone_info, drone_izen_jabe=drone_izen_jabe)
    
    elif request.method == "POST":
        bot = request.form.get('botoia')
        baimenak=[]
        error=None
        sentsoreak = []

        # "Sentsore gehitu" botoia
        if bot == '2':
            sentsore_guztiak = database.get_Sentsoreak_table()
            sentsoreak = []
            for sentsore in sentsore_guztiak:
                if sentsore.sents_id not in [sentsore_in.sents_id for sentsore_in in drone_info.drone_sentsoreak]:
                    sentsoreak.append(sentsore)

        # "Partekatu" botoia
        elif bot == '3':
            baimen_info=database.get_Baimenak_table()
            for row in baimen_info:
                for baimen in row:
                    if baimen not in ["Admin","Jabea"]:
                        baimenak.append(baimen)

        
        elif bot == '4':
            izena = request.form.get('izen')
            mota = request.form.get('mota')
            deskribapena = request.form.get('deskribapena')
            database.aldatu_dronea(izena,mota,deskribapena,drone_id)
            if not drone_info.drone_info.drone_izen == izena:
                return redirect(url_for('izen_aldaketa', drone=drone_izen_jabe, izen_berri=izena))

        # Sentsore berriak sartzeko "Sartu" botoia
        elif bot == '5':
            sens = request.form.getlist("sentsorea")
            print("SENS: SENS:")
            print(sens)
            
            database.sentsoreak_esleitu(drone_id,sens)
        
        elif bot == '6':
            partekatu_erab = request.form.get('partekatu_erab')
            baimena = request.form.get('baimena')
            database.dronea_partekatu(drone_id, partekatu_erab, baimena)
            
        drone_info = database.lortu_drone_info_osoa(drone_id)

    return render_template('modify_drone.html', drone_info=drone_info, drone_izen_jabe=drone_izen_jabe, aukera=bot, baimenak=baimenak, error=error, sentsoreak=sentsoreak)