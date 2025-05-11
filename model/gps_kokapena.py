import json

class gps_kokapena():
    
    gpsKokap_id = 0
    gpsKokap_drone = None
    gpsKokap_long = 0.0
    gpsKokap_lat = 0.0
    gpsKokap_alt = 0.0
    gpsKokap_head = 0.0
    gpsKokap_timestmp = None
    gpsKokap_norantz = ""

    def __init__(self, gpsKokapDatuArray, drone):
        self.gpsKokap_id = gpsKokapDatuArray[0]
        self.gpsKokap_drone = drone
        self.gpsKokap_long = gpsKokapDatuArray[2]
        self.gpsKokap_lat = gpsKokapDatuArray[3]
        self.gpsKokap_alt = gpsKokapDatuArray[4]
        self.gpsKokap_head = gpsKokapDatuArray[5]
        self.gpsKokap_timestmp = gpsKokapDatuArray[6]
        self.gpsKokap_norantz = gpsKokapDatuArray[7]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)