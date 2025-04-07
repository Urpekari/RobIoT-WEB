import folium
import folium.map
from folium import plugins
from folium import JsCode
from folium.plugins import Realtime

#from view.droneViewer import *
from controller.database_controller import *
import app

class mapPage():

    realPath = []
    pastWaypoints = []
    droneName = ""
    droneType = ""
    droneID = 1

    def __init__(self, droneID):
        dbOutput = app.getDBOutput()
        self.droneID = droneID
        self.realPath = dbOutput.getRealLocations(droneID)
        self.droneName = dbOutput.getDroneName(droneID)[0][0]
        self.droneType = dbOutput.getDroneType(droneID)[0][0]
        self.pastWaypoints = dbOutput.get_waypoint_past(droneID)
        self.nextWaypoints = dbOutput.get_waypoint_future(droneID)
        self.bannedAreas = dbOutput.get_banned_areas(self.droneType)
        self.restrictedAreas = dbOutput.get_restricted_areas(self.droneType)


    def waypointakMarkatu(self, pastWPs, futureWPs, futureLine):
        if len(self.pastWaypoints) > 0:
            
            # Hasierako waypoint-a
            folium.Marker(
                location=self.pastWaypoints[0],
                tooltip="Home point: {}".format(self.pastWaypoints[0]),
                popup="Home at {} for {}".format(self.pastWaypoints[0], self.droneName),
                icon=folium.Icon(color='black', icon_color='#FFB60C',prefix="fa", icon="house")
            ).add_to(pastWPs)
            
            # Pasatutako tarteko waypointak
            for wp in self.pastWaypoints[1:]:
                folium.Marker(
                    location=wp,
                    tooltip="Past waypoint: {}".format(wp),
                    popup="Waypoint at {} past by {}".format(wp, self.droneName),
                    icon=folium.Icon(color='orange', icon_color='#1c1c1c',prefix="fa", icon="flag")
                ).add_to(pastWPs)

        if len(self.nextWaypoints) > 0:

            folium.Marker(
                location=self.nextWaypoints[0],
                tooltip="Goal point: {}".format(self.nextWaypoints[0]),
                popup="Goal at {} for {}".format(self.nextWaypoints[0], self.droneName),
                icon=folium.Icon(color='darkpurple', icon_color='#FcFcFc',prefix="fa", icon="compass")
            ).add_to(futureWPs)

            if len(self.nextWaypoints) > 1:
                for wp in self.nextWaypoints[1:-1]:
                    folium.Marker(
                        location=wp,
                        tooltip="Waypoint: {}".format(wp),
                        popup="Waypoint at {} for {}".format(wp, self.droneName),
                        icon=folium.Icon(color='purple', icon_color='#1c1c1c',prefix="fa", icon="compass")
                    ).add_to(futureWPs)

                # Etorkizuneko ibilbidea dronetik hasiko da, dronearen GPS datuak baditugu.
                if len(self.realPath) > 0:
                    remainingPath = [self.realPath[-1]] + self.nextWaypoints[:]
                else:
                    remainingPath = self.nextWaypoints[:]

                folium.PolyLine(remainingPath, tooltip="Path to be followed {}".format(self.droneName), color='#DC267F', opacity=0.6, dash_array=10).add_to(futureLine)

            folium.Marker(
                location=self.nextWaypoints[-1],
                tooltip="Goal point: {}".format(self.nextWaypoints[-1]),
                popup="Goal at {} for {}".format(self.nextWaypoints[-1], self.droneName),
                icon=folium.Icon(color='black', icon_color='#DC267F',prefix="fa", icon="flag-checkered")
            ).add_to(futureWPs)
        

    def ibilbideaMarkatu(self, m, realLine):
        
        folium.plugins.BoatMarker(
            location=(self.realPath[-1]),
            heading=45,
            color="#FFB60C"
        ).add_to(m)
        
        folium.Marker(
            location=self.realPath[-1],
            tooltip="Latest",
            popup="Latest known position for {} - {}".format(self.droneName, self.realPath[-1]),
            icon=folium.Icon(color='black', icon_color='#FFB60C', prefix="fa", icon=self.droneType.lower()),
        ).add_to(m)
        folium.plugins.AntPath(self.realPath, tooltip="Path followed by {}".format(self.droneName), color='#FFB60C', dash_array=[30, 50]).add_to(realLine)
        
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
            m = folium.Map((self.realPath[-1]), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap",
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
            folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
        )

        m.get_root().render()
        header = m.get_root().header.render()
        body_html = m.get_root().html.render()
        script = m.get_root().script.render()

        return header, body_html, script

class mapInit():
    def map_empty():
        m = folium.Map((43.263973, -2.951087), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

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
    
    def map_with_pointers(list):
        coords=list[-1]
        listfloat=[]
        m = folium.Map((float(coords[0]),float(coords[1])), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 
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
        
        folium.PolyLine(listfloat, tooltip="Path that will be followed", color='#FFB60C').add_to(m)

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

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