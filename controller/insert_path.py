import re
from datetime import datetime

from flask import *

from view.mapPage import *
from controller.database_controller import *
from view.mapinit import *
from view.mapplan import *

import tkinter as tk

#from view.droneViewer import *
from controller.database_controller import *
import app

class insertPath():
    def insertWaypoints(drone, droneID):

        mapplanpage = mapPlan(droneID)

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

                    print("BOT 1")
                    print(list)
                    if list:
                        header, body_html, script=mapplanpage.map_with_pointers(list)
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
                
                    print("BOT 2")
                    print(list)
                    if list:
                        header, body_html, script=mapplanpage.map_with_pointers(list)
                    else:
                        header, body_html, script=mapInit.map_empty()
                    return render_template("insert_path.html", header=header, body_html=body_html, script=script, lat=lat, long=long, list=list, error=error, dronea=drone)
                
                elif bot == '3':
                    droneak,id=app.get_erab_drone_list(session['erabiltzailea'])
                    
                    print("ID")
                    print(id)
                    print(droneak)
                    print("Lo que le damos")
                    print(drone)

                   
                    # Hau kendu behar dugu
                    for coords in list:
                        app.dbinput.insert_GPS_kokapena(droneID,coords[1],coords[0],None,datetime.now(),"UPF")
                    
                    return redirect(url_for('control'))
                
                elif bot == '4':
                    rm_coords=request.form.get('rm_coord')
                    coords = re.findall('\'(.*?)\'',rm_coords)
                    list.remove(coords)

                    if list:
                        header, body_html, script=mapplanpage.map_with_pointers(list)
                    else:
                        header, body_html, script=mapInit.map_empty()
                    
                    return render_template("insert_path.html", header=header, body_html=body_html, script=script, lat=lat, long=long, list=list, error=error, dronea=drone)

        except KeyError as e:
            return redirect(url_for('index'))
