import json

class droneak():
    
    drone_id = 0
    drone_izen = ""
    drone_mota = ""
    drone_desk = ""

    def __init__(self, droneDatuArray):
        self.drone_id = droneDatuArray[0]
        self.drone_izen = droneDatuArray[1]
        self.drone_mota = droneDatuArray[2]
        self.drone_desk = droneDatuArray[3]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)