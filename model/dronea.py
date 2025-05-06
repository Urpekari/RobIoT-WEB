import json

# Drone-erabiltzaile partekatzeen lotura

class dronea():
    drone_id = 0
    drone_izen = ""
    drone_mota = ""
    drone_desk = ""
    drone_sentsoreak = []
    drone_jabea = None
    drone_kontroladoreak = []

    def __init__(self, droneDatuArray, droneSentsoreArray, jabea, kontroladoreak):
        self.drone_id = droneDatuArray[0]
        self.drone_izen = droneDatuArray[1]
        self.drone_mota = droneDatuArray[2]
        self.drone_desk = droneDatuArray[3]
        self.drone_sentsoreak = droneSentsoreArray
        self.drone_jabea = jabea
        self.drone_kontroladoreak = kontroladoreak

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)