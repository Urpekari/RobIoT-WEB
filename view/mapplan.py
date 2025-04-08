import folium
from view.mapPage import *

from controller.database_controller import *
import app

class mapPlan():

    def __init__(self, droneID):
        self.dbOutput = app.dboutput
        self.allWaypoints = self.dbOutput.get_all_waypoints(droneID)
    
    def map_with_pointers(self, list):
        coords=list[-1]
        listfloat=[]
        m = folium.Map((float(coords[0]),float(coords[1])), zoom_start=16) # "cartodb positron", "cartodb darkmatter", "openstreetmap", 
        
        gordetakoWPs = folium.FeatureGroup("Past Waypoints").add_to(m)
        print("Gordetako WP-ak bilatzen!")
        gordetakoWPCoords = self.allWaypoints
        print(gordetakoWPCoords)
        if len(gordetakoWPCoords) >= 1:
            for wp in gordetakoWPCoords:        
                    folium.Marker(
                        location=wp,
                        tooltip="Waypoint: {}".format(wp),
                        popup="Previously created waypoint at {}".format(wp),
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