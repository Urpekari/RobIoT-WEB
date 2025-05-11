import folium
from view.mapPage import *

import multimethod

from controller.database_controller import *
import app

class mapPlan():

    # TODO: CONTROLLER-EAN SARTU
    # GPS balio guztien artean waypoint-ak soilik hartzeko
    def __filterWaypoints(self:object, rawGpsData:list, isPastWP:bool):
        waypoints = []
        for gpsPoint in rawGpsData:
            if gpsPoint.gps_way == True and gpsPoint.gps_past == isPastWP:
                waypoints.append(gpsPoint)
        return waypoints
    
    def __filterForWaypoints(self:object, rawGpsData:list):
        waypoints = []
        for gpsPoint in rawGpsData:
            if gpsPoint.gps_way == True:
                waypoints.append(gpsPoint)
        return waypoints
    
    # TODO: CONTROLLER-EAN SARTU
    # GPS balioetatik koordenatuak lortzeko, zerrenda luze baten
    def __filterSimplePath(self, rawGpsData):
        waypoints = []
        for gpsPoint in rawGpsData:
            waypoints.append(gpsPoint.get_gps_coords())
        print(waypoints)
        return waypoints

    # TODO: CONTROLLER-EAN SARTU
    # GPS balio guztien artean dronearen benetako posizioak soilik hartzeko
    def __filterPositionLogs(self, rawGpsData):
        posLog = []
        for gpsPoint in rawGpsData:
            if gpsPoint.gps_way == False:
                posLog.append(gpsPoint)
        return posLog

    def __init__(self, droneID):
        self.database = app.database
        self.drone = self.database.lortu_dronea(droneID)
        self.gpsData = self.database.lortu_drone_GPS_informazioa(droneID)

        self.realPath = self.__filterPositionLogs(self.gpsData)
        self.simplePath = self.__filterSimplePath(self.realPath)

        self.allWaypoints = self.__filterForWaypoints(self.gpsData)
        self.simpleAllWaypoints = self.__filterSimplePath(self.allWaypoints)

        self.pastWaypoints = self.__filterWaypoints(self.gpsData, isPastWP=True)
        self.simplePastWaypoints = self.__filterSimplePath(self.pastWaypoints)

        self.nextWaypoints = self.__filterWaypoints(self.gpsData, isPastWP=False)
        self.simpleNextWaypoints = self.__filterSimplePath(self.nextWaypoints)

    
    def map_with_pointers(self, list):
        
        listfloat=[]

        if(len(list)>0):
            coords=list[-1]
        else:
             if len(self.allWaypoints) > 0:
                 coords=self.allWaypoints[-1].get_gps_coords()
             else:
                 coords=[43.263973, -2.951087]
        
        m = folium.Map((float(coords[0]),float(coords[1])), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 
        
        gordetakoWPs = folium.FeatureGroup("Past Waypoints").add_to(m)
        if len(self.allWaypoints) >= 1:
            for wp in self.allWaypoints:        
                    folium.Marker(
                        location=wp.get_gps_coords(),
                        tooltip="Waypoint: {}".format(wp.get_gps_coords()),
                        popup="Previously created waypoint at {}".format(wp.get_gps_coords()),
                        icon=folium.Icon(color='purple', icon_color='#1c1c1c',prefix="fa", icon="compass")
                    ).add_to(gordetakoWPs)
        
        for coord in list:
            coord = [float(coord[0]),float(coord[1])]
            folium.Marker(
                location=coord,
                tooltip="New waypoint: {}".format(coord),
                popup="New waypoint at {}".format(coord),
                icon=folium.Icon(color='orange', icon_color='#1c1c1c',prefix="fa", icon="flag")
            ).add_to(m)
            listfloat.append(coord)
            if listfloat[0]==[]:
                listfloat=listfloat[1:]
        
        if len(self.allWaypoints) > 1:
            folium.PolyLine(self.simpleAllWaypoints, tooltip="Already set path", color='#DC267F', opacity=0.6, dash_array=10).add_to(m)

            if len(listfloat) >= 1:
                folium.PolyLine([self.allWaypoints[-1].get_gps_coords(), listfloat[0]], tooltip="Already set path", color='#FFB60C').add_to(m)


        if len(listfloat) > 1:
            folium.PolyLine(listfloat, tooltip="Path that will be followed", color='#FFB60C').add_to(m)

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

        # Jada existitzen diren waypoint-ak mapan agertzeko:
        # Honek EZ DITU zerrendan jartzen! Kontuz! Hori agian interesgarria da ere!

        m.add_child(
            folium.LatLngPopup()
        )

        m.add_child(
            folium.ClickForLatLng(format_str='lat + "," + lng', alert=False)
        )

        m.get_root().render()
        header = m.get_root().header.render()
        body_html = m.get_root().html.render()
        script = m.get_root().script.render()

        return header, body_html, script