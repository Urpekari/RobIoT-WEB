import json

class erabiltzailea():
    
    erab_id = 0
    erab_izen = ""
    erab_abizen = ""
    erab_email = ""

    def __init__(self, erabDatuArray):
        self.erab_id = erabDatuArray[0]
        self.erab_izen = erabDatuArray[1]
        self.erab_abizen = erabDatuArray[2]
        self.erab_email = erabDatuArray[4]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)