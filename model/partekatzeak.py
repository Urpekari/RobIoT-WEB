import json

# partekatze-erabiltzaile partekatzeen lotura

class partekatzeak():
    partekatze_id = 0
    partekatze_erab = None
    partekatze_drone = None
    partekatze_baimen = ""

    def __init__(self, partekatzeDatuArray, erab, drone):
        self.partekatze_id = partekatzeDatuArray[0]
        self.partekatze_erab = erab
        self.partekatze_drone = drone
        self.partekatze_baimen = partekatzeDatuArray[3]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)