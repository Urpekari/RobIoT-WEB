import json

class drone_sentsore():
    
    drone_sentsore_id = 0
    drone_sentsore_ezizen = ""
    drone_sentsore_drone = None
    drone_sentsore_sentsore = None

    def __init__(self, drone_sentsoreDatuArray, drone, sentsore):
        self.drone_sentsore_id = drone_sentsoreDatuArray[0]
        self.drone_sentsore_ezizen = drone_sentsoreDatuArray[1]
        self.drone_sentsore_drone = drone
        self.drone_sentsore_sentsore = sentsore

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)