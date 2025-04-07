import other.banned_areas as bans

class tables():
    Baimenak="Baimenak"
    Droneak="Droneak"
    Drone_Sentsore="Drone_Sentsore"
    Erabiltzaileak="Erabiltzaileak"
    Mezuak="Mezuak"
    Partekatzeak="Partekatzeak"
    GPS_kokapena="GPS_kokapena"
    Sentsoreak="Sentsoreak"
    Sentsore_info="Sentsore_info"

    Baimenak_header=["ID"]
    Droneak_header=["ID","Izena","Mota","Deskribapena"]
    Drone_Sentsore_header=["ID","Ezizena","Drone","Sentsore"]
    Erabiltzaileak_header=["ID","Izena","Abizenak","Pasahitza","email","Dokumentuak"]
    Mezuak_header=["ID","Drone","Edukia","Timestamp"]
    Partekatzeak_header=["ID","Erabiltzailea","Drone","Baimen mota"]
    GPS_kokapena_header=["ID","Drone","Longitude","Latitude","Timestamp"]
    Sentsoreak_header=["ID","Izena","Mota","Deskribapena"]
    Sentsore_info_header=["ID","Drone","Sentsore","Balioa","Timestamp"]

class output():
    _instance = None

    def __init__(self,mysql):
        self.mysql=mysql

    def get_info(self,name):
        cur = self.mysql.connection.cursor()
        query = "SELECT * FROM {0}".format(name)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results

    def create_csv(self,name):
        csv_array=[]
        array=self.get_info(name)
        for row in array:
            for column in row:
                csv_array.append(str(column))
                csv_array.append(';')
            csv_array=csv_array[:-1]
            csv_array.append('\n')
        return csv_array
    
    def erabiltzailea_egiaztatu(self,username, password):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE Izen = %s AND Pasahitza = %s", (username, password))
        usuario = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return True if usuario else False
    
    def get_drone_id(self,izena,mota,deskribapena):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE Izena = %s AND Mota = %s AND Deskribapena = %s", (izena,mota,deskribapena))
        drone = cur.fetchall()
        cur.close()
        return drone[-1][0]
    
    def get_erab_id(self,izena):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE Izen = %s", (izena,))
        usuario = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return usuario[0]
    
    def get_erab_izen(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Izen FROM Erabiltzaileak WHERE idErabiltzaileak = %s", (id_erab,))
        erab_izen = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return erab_izen[0]
    
    def get_sentsore_id(self,izena):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak WHERE Izen = %s", (izena,))
        sents = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return sents[0]
    
    def get_erab_droneak(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (id_erab,))
        erab_dron = cur.fetchall() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return [sublist[2] for sublist in erab_dron], [sublist[3] for sublist in erab_dron]
    
    def get_drone_info(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE idDroneak = %s", (id_drone,))
        drone = cur.fetchone()
        cur.close()
        return drone[1]

    def get_drone_jabe(self,id_dron):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s", (id_dron,"Jabea"))
        jabe_dron = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return jabe_dron
    
    def get_drone_GPS(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM GPS_kokapena WHERE Droneak_idDroneak = %s", (id_drone,))
        GPS_drone = cur.fetchall() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return GPS_drone[-1]

    def get_drone_mezuak(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Mezuak WHERE Droneak_idDronek = %s", (id_drone,))
        mezu_drone = cur.fetchall() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return mezu_drone
    
    def get_drone_sentsore(self,id_drone,id_sentsore):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Drone_Sentsore WHERE Droneak_idDronek = %s AND Sentsoreak_idSentsoreak = %s", (id_drone,id_sentsore))
        dron_sens = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return dron_sens
    
    def get_sentsore_info(self,id_dron_sens):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsore_info WHERE Drone_Sentsore_idDroneSentsore = %s", (id_dron_sens,))
        sens_info = cur.fetchall() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        return sens_info[-1]

    # Maparekin erabiltzeko atalak

    def getRealLocations(self, droneID):
        cur = self.mysql.connection.cursor()
        query = "SELECT Latitude, Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s"
        cur.execute(query,(droneID, "DOW"))
        results = cur.fetchall()
        cur.close()
        return results
    
    def getDroneType(self, droneID):
        cur = self.mysql.connection.cursor()
        query = "SELECT Mota FROM Droneak WHERE idDroneak = {}".format(droneID)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    
    def getDroneName(self, droneID):
        cur = self.mysql.connection.cursor()
        query = "SELECT izena FROM Droneak WHERE idDroneak = {}".format(droneID)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    
    def get_latitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Latitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s " )
        cur.execute(query,(droneID,dir))
        lats = cur.fetchall()
        cur.close()
        return lats

    def get_longitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s ")
        cur.execute(query,(droneID,dir))
        lons = cur.fetchall()
        cur.close()
        return lons
    
    def get_altitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Altitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s " )
        cur.execute(query,(droneID,dir))
        lats = cur.fetchall()
        cur.close()
        return lats

    def get_waypoints(self, droneID, dir):
        lats = self.get_latitudes(droneID, dir)
        lons = self.get_longitudes(droneID, dir)
        waypoints = []
        if len(lats) == len(lons):
            for i in range(len(lats)):
                waypoints.append([lats[i][0], lons[i][0]])
        return waypoints
    
    def get_waypoints_full(self, droneID, dir):
        lats = self.get_latitudes(droneID, dir)
        lons = self.get_longitudes(droneID, dir)
        alts = self.get_altitudes(droneID, dir)
        waypoints = []
        if len(lats) == len(lons):
            for i in range(len(lats)):
                waypoints.append([lats[i][0], lons[i][0], alts[i][0]])
        return waypoints

    def get_next_waypoint(self, droneID):
        waypoints = self.get_waypoints_full(droneID, "UPF")
        return(waypoints[0])
        
    def get_waypoint_past(self, droneID):
        waypoints = self.get_waypoints(droneID, "UPP")
        return waypoints

    def get_waypoint_future(self, droneID):
        waypoints = self.get_waypoints(droneID, "UPF")
        return waypoints

    def get_banned_areas(self, droneType):
        if droneType.lower() == "plane":
            return(bans.planeBans)
    
    def get_restricted_areas(self, droneType):
        if droneType.lower() == "plane":
            return(bans.planeLimits)

class input():
    _instance = None

    def __init__(self,mysql):
        self.mysql=mysql

    def insert_Drone_Sentsore(self,ezizen,id_drone,id_sents):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Drone_Sentsore (Ezizena,Droneak_idDroneak,Sentsoreak_idSentsoreak) VALUES (%s,%s,%s)"
        cur.execute(query,(ezizen,id_drone,id_sents))
        self.mysql.connection.commit()
        cur.close()

    def insert_Droneak(self,izena,mota,deskribapena):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Droneak (Izena,Mota,Deskribapena) VALUES (%s,%s,%s)"
        cur.execute(query,(izena,mota,deskribapena))
        self.mysql.connection.commit()
        cur.close()

    def insert_Erabiltzaileak(self,izena, abizena, pasahitza, email, dokumentuak):
        try:
            cursor = self.mysql.connection.cursor()
            query = "INSERT INTO Erabiltzaileak (Izen, Abizena, Pasahitza, Email, Hegan_egiteko_baimena) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (izena, abizena, pasahitza, email, dokumentuak))
            self.mysql.connection.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            cursor.close()

    def insert_GPS_kokapena(self,id_drone,lng,ltd,alt,timestamp,noranzkoa):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO GPS_kokapena (Droneak_idDroneak,Longitude,Latitude,Altitude,Timestamp,Noranzkoa) VALUES (%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(id_drone,lng,ltd,alt,timestamp,noranzkoa))
        self.mysql.connection.commit()
        cur.close()

    def insert_Mezuak(self,id_drone,edukia,timestamp,noranzkoa):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Mezuak (Droneak_idDroneak,Eduikia,Timestamp,Noranzkoa) VALUES (%s,%s,%s,%s)"
        cur.execute(query,(id_drone,edukia,timestamp,noranzkoa))
        self.mysql.connection.commit()
        cur.close()

    def insert_Partekatzeak(self,id_erabiltzaile,id_drone,baimena):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Partekatzeak (Erabiltzaileak_idErabiltzaileak,Droneak_idDroneak,Baimenak_idBaimenak) VALUES (%s,%s,%s)"
        cur.execute(query,(id_erabiltzaile,id_drone,baimena))
        self.mysql.connection.commit()
        cur.close()

    def insert_Sentsore_info(self,id_drone_sents,balioa,timestamp):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Sentsore_info (Dronea_Sentsore_idDroneSentsore,Balioa,Timestamp) VALUES (%s,%s,%s)"
        cur.execute(query,(id_drone_sents,balioa,timestamp))
        self.mysql.connection.commit()
        cur.close()

    def insert_Sentsoreak(self,izena,mota,deskribapena):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Sentsoreak (Izena,Mota,Deskribapena) VALUES (%s,%s,%s)"
        cur.execute(query,(izena,mota,deskribapena))
        self.mysql.connection.commit()
        cur.close()