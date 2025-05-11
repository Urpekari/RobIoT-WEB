import folium
import folium.map
from folium import plugins
from folium import JsCode
from folium.plugins import Realtime

import multimethod

#from view.droneViewer import *
from controller.database_controller import *
import app

class mapPage():

    realPath = []
    pastWaypoints = []
    drone = None

    # TODO: CONTROLLER-EAN SARTU
    # GPS balio guztien artean waypoint-ak soilik hartzeko
    def __filterWaypoints(self:object, rawGpsData:list, isPastWP:bool):
        waypoints = []
        for gpsPoint in rawGpsData:
            if gpsPoint.gps_way == True and gpsPoint.gps_past == isPastWP:
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

    def __init__(self, database, droneID):
        self.drone = database.lortu_dronea(droneID)
        self.droneID = self.drone.drone_id
        self.droneName = self.drone.drone_izen
        self.droneType = self.drone.drone_mota
        
        self.gpsData = database.lortu_drone_GPS_informazioa(self.drone.drone_id)

        self.realPath = self.__filterPositionLogs(self.gpsData)
        self.simplePath = self.__filterSimplePath(self.realPath)

        self.pastWaypoints = self.__filterWaypoints(self.gpsData, isPastWP=True)
        self.simplePastWaypoints = self.__filterSimplePath(self.pastWaypoints)

        self.nextWaypoints = self.__filterWaypoints(self.gpsData, isPastWP=False)
        self.simpleNextWaypoints = self.__filterSimplePath(self.nextWaypoints)

        self.bannedAreas, self.restrictedAreas = database.lortu_azalerak(self.droneType)

    def waypointakMarkatu(self, pastWPs, futureWPs, futureLine):
        if len(self.pastWaypoints) > 0:
            
            # Hasierako waypoint-a
            folium.Marker(
                location=self.pastWaypoints[0],
                tooltip="Home point: {}".format(self.pastWaypoints[0].get_gps_coords()),
                popup="Home at {} for {}".format(self.pastWaypoints[0].get_gps_coords(), self.droneName),
                icon=folium.Icon(color='black', icon_color='#FFB60C',prefix="fa", icon="house")
            ).add_to(pastWPs)
            
            # Pasatutako tarteko waypointak
            for wp in self.pastWaypoints[1:]:
                folium.Marker(
                    location=wp.get_gps_coords(),
                    tooltip="Past waypoint: {}".format(wp.get_gps_coords()),
                    popup="Waypoint at {} past by {}".format(wp.get_gps_coords(), self.droneName),
                    icon=folium.Icon(color='orange', icon_color='#1c1c1c',prefix="fa", icon="flag")
                ).add_to(pastWPs)

        if len(self.nextWaypoints) > 0:

            if len(self.nextWaypoints) >= 1:
                for wp in self.nextWaypoints[1:-1]:
                    folium.Marker(
                        location=wp.get_gps_coords(),
                        tooltip="Waypoint: {}".format(wp.get_gps_coords()),
                        popup="Waypoint at {} for {}".format(wp.get_gps_coords(), self.droneName),
                        icon=folium.Icon(color='purple', icon_color='#1c1c1c',prefix="fa", icon="compass")
                    ).add_to(futureWPs)

                # Etorkizuneko ibilbidea dronetik hasiko da, dronearen GPS datuak baditugu.
                #print("Interesezko atala")
                #print(len(self.realPath))
                
                if len(self.realPath) > 0:
                    remainingPath = [self.simplePath[-1]] + self.simpleNextWaypoints[:]
                else:
                    remainingPath = self.simpleNextWaypoints[:]

                folium.PolyLine(remainingPath, tooltip="Path to be followed {}".format(self.droneName), color='#DC267F', opacity=0.6, dash_array=10).add_to(futureLine)

            folium.Marker(
                location=self.nextWaypoints[0].get_gps_coords(),
                tooltip="Current target point: {}".format(self.nextWaypoints[0].get_gps_coords()),
                popup="Next waypoint for {} at {}".format(self.droneName, self.nextWaypoints[0].get_gps_coords()),
                icon=folium.Icon(color='darkpurple', icon_color='#FcFcFc',prefix="fa", icon="compass")
            ).add_to(futureWPs)

            folium.Marker(
                location=self.nextWaypoints[-1].get_gps_coords(),
                tooltip="Goal point: {}".format(self.nextWaypoints[-1].get_gps_coords()),
                popup="Goal at {} for {}".format(self.nextWaypoints[-1].get_gps_coords(), self.droneName),
                icon=folium.Icon(color='black', icon_color='#DC267F',prefix="fa", icon="flag-checkered")
            ).add_to(futureWPs)
        
    # Aukeratutako dronearen ID-a erakusten
    def getDroneID(self):
        return(self.droneID)

    def ibilbideaMarkatu(self, m, realLine):

        print(self.realPath[-1].get_gps_heading())

        folium.plugins.BoatMarker(
            location=(self.realPath[-1].get_gps_coords()),
            heading=self.realPath[-1].get_gps_heading(),
            color="#FFB60C"
        ).add_to(m)
        
        folium.Marker(
            location=self.realPath[-1].get_gps_coords(),
            tooltip="Latest",
            popup="Latest known position for {} - {}".format(self.droneName, self.realPath[-1].get_gps_coords()),
            icon=folium.Icon(color='black', icon_color='#FFB60C', prefix="fa", icon=self.droneType.lower()),
        ).add_to(m)
        folium.plugins.AntPath(self.simplePath, tooltip="Path followed by {}".format(self.droneName), color='#FFB60C', dash_array=[30, 50]).add_to(realLine)

    def debekuakMarkatu(self, m):

        bans = folium.FeatureGroup("Banned areas").add_to(m)
        limits = folium.FeatureGroup("Restricted operation").add_to(m)

        if self.restrictedAreas:
            for center in self.restrictedAreas:
                tooltip = center[4]
                radius=center[2]
                if center[3] > 0:
                    maxAltitude = center[3]
                    popup = "Maximum altitude: {}m".format(maxAltitude)
                else:
                    popup = "Specific and special permission required."
                    
                folium.Circle(
                    location=[center[0], center[1]],
                    radius=radius,
                    color="orange",
                    weight=1,
                    fill_opacity=0.4,
                    opacity=1,
                    fill_color="orange",
                    fill=False,  # gets overridden by fill_color
                    popup=popup,
                    tooltip=tooltip,
                ).add_to(limits)

        if self.bannedAreas:
            for center in self.bannedAreas:
                tooltip = center[4]
                radius=center[2]
                folium.Circle(
                    location=[center[0], center[1]],
                    radius=radius,
                    color="darkpurple",
                    weight=1,
                    fill_opacity=0.4,
                    opacity=1,
                    fill_color="purple",
                    fill=False,  # gets overridden by fill_color
                    popup=tooltip,
                    tooltip=tooltip,
                ).add_to(bans)

    def map(self):

        if len(self.realPath) > 0:
            m = folium.Map((self.realPath[-1].get_gps_coords()), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap",
            realLine = folium.FeatureGroup("Real followed path").add_to(m)
            self.ibilbideaMarkatu(m, realLine)
        else:
            m = folium.Map((43.263973, -2.951087), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap",

        pastWPs = folium.FeatureGroup("Past Waypoints").add_to(m)
        futureWPs = folium.FeatureGroup("Next Waypoints").add_to(m)
        futureLine = folium.FeatureGroup("Future estimated path").add_to(m)
        restrictions = folium.FeatureGroup("Restricted and banned areas").add_to(m)

        self.waypointakMarkatu(pastWPs, futureWPs, futureLine)
        self.debekuakMarkatu(restrictions)

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

        m.add_child(
            folium.LatLngPopup()
        )

        m.add_child(
            folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=False)
        )

        m.get_root().render()
        header = m.get_root().header.render()
        body_html = m.get_root().html.render()
        script = m.get_root().script.render()

        return header, body_html, script

