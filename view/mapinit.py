import folium
import folium.map
from folium import plugins
from folium import JsCode
from folium.plugins import Realtime

#from view.droneViewer import *
from controller.database_controller import *
import app

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
