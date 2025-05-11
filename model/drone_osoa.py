import json

# Drone-erabiltzaile partekatzeen lotura

class drone_osoa():
    drone_info = None
    drone_sentsoreak = []
    drone_jabea = None
    drone_kontroladoreak = []
    drone_ikusleak = []

    def __init__(self, droneDatuak, droneSentsoreArray, jabea, kontroladoreak, ikusleak):
        self.drone_info = droneDatuak
        self.drone_sentsoreak = droneSentsoreArray
        self.drone_jabea = jabea
        self.drone_kontroladoreak = kontroladoreak
        self.drone_ikusleak = ikusleak

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)