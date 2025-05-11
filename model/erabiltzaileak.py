import json

class erabiltzaileak():
    
    erab_id = 0
    erab_izen = ""
    erab_abizen = ""
    erab_email = ""
    erab_hegazkin_baimenak = ""

    def __init__(self, erabDatuArray):
        self.erab_id = erabDatuArray[0]
        self.erab_izen = erabDatuArray[1]
        self.erab_abizen = erabDatuArray[2]
        self.erab_email = erabDatuArray[4]
        self.erab_hegazkin_baimenak = erabDatuArray[5]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)