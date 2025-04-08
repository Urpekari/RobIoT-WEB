import folium
import folium.map
from folium import plugins
from folium import JsCode
from folium.plugins import Realtime

#from view.droneViewer import *
from controller.database_controller import *
import app

class planPage():
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

    def map_with_pointers(self, list):
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

        pastWPs = folium.FeatureGroup("Past Waypoints").add_to(m)
        futureWPs = folium.FeatureGroup("Next Waypoints").add_to(m)
        self.waypointakMarkatu(pastWPs, futureWPs, None)

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