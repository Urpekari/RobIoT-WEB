import folium
import folium.map
from flask_mysqldb import MySQL
from flask import render_template, render_template_string

#from view.droneViewer import *
from controller.dataSim import *
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
        datasim = dataSim()
        self.realPath = dbOutput.getRealLocations(droneID)
        self.droneName = dbOutput.getDroneName(droneID)[0][0]
        self.droneType = dbOutput.getDroneType(droneID)[0][0]
        self.pastWaypoints = datasim.getPastWaypoints(droneID)
        self.nextWaypoints = datasim.getNextWaypoints(droneID)
        self.bannedAreas = datasim.getBannedAreas(self.droneType)

    def map(self, droneID):
        """Embed a map as an iframe on a page."""
        m = folium.Map((self.realPath[-1]), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 
        # __init__ constructor!
        data = dataSim()

        pastWPs = folium.FeatureGroup("Past Waypoints").add_to(m)
        nextWPs = folium.FeatureGroup("Next Waypoints").add_to(m)

        folium.PolyLine(self.realPath, tooltip="Path followed by {}".format(self.droneName), color='#FFB60C').add_to(pastWPs)

        # Oraingo posizioa.
        print(self.droneType)
        folium.Marker(
            location=self.realPath[-1],
            tooltip="Latest",
            popup="Latest known position for {}".format(self.droneName),
            icon=folium.Icon(color='black', icon_color='#FFB60C', prefix="fa", icon=self.droneType.lower()),
        ).add_to(m)

        # Hasierako waypoint-a
        folium.Marker(
            location=self.pastWaypoints[0],
            tooltip="Home point: {}".format(self.pastWaypoints[0]),
            popup="Home at {} for {}".format(self.pastWaypoints[0], self.droneName),
            icon=folium.Icon(color='black', icon_color='#FFB60C',prefix="fa", icon="house")
        ).add_to(pastWPs)

        # Tarteko waypoint guztiak
        # Lehenik pasatu ditugunak jada:
        for wp in self.pastWaypoints[1:]:
            folium.Marker(
                location=wp,
                tooltip="Past waypoint: {}".format(wp),
                popup="Waypoint at {} past by {}".format(wp, self.droneName),
                icon=folium.Icon(color='orange', icon_color='#1c1c1c',prefix="fa", icon="flag")
            ).add_to(pastWPs)

        # pasatu behar ditugunak
        for wp in self.nextWaypoints[0:-1]:
            folium.Marker(
                location=wp,
                tooltip="Waypoint: {}".format(wp),
                popup="Waypoint at {} for {}".format(wp, self.droneName),
                icon=folium.Icon(color='purple', icon_color='#1c1c1c',prefix="fa", icon="compass")
            ).add_to(nextWPs)

        remainingPath = [self.realPath[-1]] + self.nextWaypoints[:]
        folium.PolyLine(remainingPath, tooltip="Path to be followed {}".format(self.droneName), color='#DC267F', opacity=0.6, dash_array=10).add_to(nextWPs)

        # Amaierako waypointa
        folium.Marker(
            location=self.nextWaypoints[-1],
            tooltip="Home point: {}".format(self.nextWaypoints[-1]),
            popup="Homne at {} for {}".format(self.nextWaypoints[-1], self.droneName),
            icon=folium.Icon(color='black', icon_color='#DC267F',prefix="fa", icon="flag-checkered")
        ).add_to(nextWPs)

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

        #iframe = m.get_root()._repr_html_()

        #folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")


        #return render_template("map.html", iframe=iframe)

        m.get_root().render()
        header = m.get_root().header.render()
        body_html = m.get_root().html.render()
        script = m.get_root().script.render()

        m.add_child(
            #folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
            folium.LatLngPopup()
        )

        m.save('templates/map1.html')

        return render_template("control.html")

 

        return map_object

class mapInit():
    def map_empty():
        m = folium.Map((43.263973, -2.951087), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 

        m.get_root().width = "1000vw"
        m.get_root().height = "650vh"
        folium.LayerControl().add_to(m)

        m.get_root().render()

        m.save('templates/map1.html')