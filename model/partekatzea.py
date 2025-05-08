import json

# partekatze-erabiltzaile partekatzeen lotura

class partekatzea():
    partekatze_id = 0
    partekatze_erab = None
    partekatze_drone = None
    partekatze_mota = ""

    def __init__(self, partekatzeDatuArray, partekatzeErab, partekatzeDrone):
        self.partekatze_id = partekatzeDatuArray[0]
        self.partekatze_erab = partekatzeErab
        self.partekatze_drone = partekatzeDrone
        self.partekatze_mota = partekatzeDatuArray[3]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)