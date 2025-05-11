import json

class sentsore_info():
    
    sentsInfo_id = 0
    sentsInfo_drone = None
    sentsInfo_balio = ""
    sentsInfo_timestmp = None

    def __init__(self, sentsInfoDatuArray, drone):
        self.sentsInfo_id = sentsInfoDatuArray[0]
        self.sentsInfo_drone = drone
        self.sentsInfo_balio = sentsInfoDatuArray[2]
        self.sentsInfo_timestmp = sentsInfoDatuArray[3]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)