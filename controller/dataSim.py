# FUNTZIO HAU GUZTIA TENPORALA DA, HAU KENDU BEHAR DUGU DB-KO GUZTIA DUGUNEAN!
class dataSim():

    locations = []

    def __init__(self):
        self.locations = []
        self.locations.append([43.35327, -3.126598])
        self.locations.append([43.353721, -3.126601])
        self.locations.append([43.353851, -3.126598])
        self.locations.append([43.354221, -3.126619])
        self.locations.append([43.354315, -3.126731])
        self.locations.append([43.355325, -3.126415])
        self.locations.append([43.355438, -3.127814])
        self.locations.append([43.355917, -3.129505])

    def getRealLocations(self, droneID):
        return self.locations
    
    def getDroneName(self, droneID):
        return "Galerna"
    
    def getDroneType(self, droneID):
        return "sailboat" # Oraingoz fontawesome-ren edozein ikono erabili daiteke.
    
    def getRealLocations(self, droneID):
        return self.locations

    def getPastWaypoints(self, droneID):
        return [[43.3533, -3.1266], [43.3542, -3.1266] ,[43.3550, -3.1266]]
    
    def getNextWaypoints(self, droneID):
        return [ [43.356236, -3.13085], [43.354236, -3.131069], [43.353209, -3.133613], [43.353240, -3.138345], [43.352237, -3.142307], [43.350692, -3.144254], [43.349986, -3.143157]]

    def getBannedAreas(self, droneType):
        return [[43.302664, -2.936193], [43.301977, -2.928736], [43.301977, -2.928736], [43.301977, -2.928736], [43.301977, -2.928736], [43.301977, -2.928736],  [43.301977, -2.928736]]