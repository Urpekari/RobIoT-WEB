import json

# Drone-erabiltzaile partekatzeen lotura

class gpspoint():
    gps_lat = 0
    gps_lng = 0
    gps_alt = 0
    gps_hdg = None
    gps_way = False
    gps_past = True
    gps_timestamp = None

    def __init__(self, rawGpsPoint):
        #print(rawGpsPoint)
        self.gps_lat = rawGpsPoint[3]
        self.gps_lng = rawGpsPoint[2]
        self.gps_alt = rawGpsPoint[4]
        self.gps_hdg = rawGpsPoint[5]
        if rawGpsPoint[7] == "DOW":
            self.gps_way = False
            self.gps_past = True

        elif rawGpsPoint[7] == "UPF":
            self.gps_way = True
            self.gps_past = False

        else:
            self.gps_way = True
            self.gps_past = True
            
        self.gps_timestamp = rawGpsPoint[6]


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def get_gps_coords(self):
        return[self.gps_lat, self.gps_lng]
    
    def get_gps_lat(self):
        return self.gps_lat
    
    def get_gps_lng(self):
        return self.gps_lng
    
    def get_gps_heading(self):
        if self.gps_hdg:
            return self.gps_hdg
        else:
            return -1
        
    def get_gps_timestamp(self):
        return(self.gps_timestamp)