import json

class mezuak():
    
    mezu_id = 0
    mezu_drone = None
    mezu_edukia = ""
    mezu_timestmp = None
    mezu_norantz = ""

    def __init__(self, mezuDatuArray, drone):
        self.mezu_id = mezuDatuArray[0]
        self.mezu_drone = drone
        self.mezu_edukia = mezuDatuArray[2]
        self.mezu_timestmp = mezuDatuArray[3]
        self.mezu_norantz = mezuDatuArray[4]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)