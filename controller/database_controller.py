import other.banned_areas as bans
from multimethod import *
from app import *

from model.erabiltzailea import erabiltzailea
from model.sentsorea import sentsorea
from model.dronea import dronea

# Klase bat badago datuak gordetzen dituena, klasea bidaltzea lehenetsiko dugu
# Adibidez, droneID edo erabiltzaile izena bidali nahi izatekotan, drone klaseko objektu bat eta erabiltzailea klaseko objektuak lehenetsiko ditugu

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
        usuario = cur.fetchone() 
        cur.close()
        return True if usuario else False
    
    def get_erab_drone_list(self, erab):
        baimenak=self.get_erab_baimen(erab)
        #baimen_drone_id = []
        droneak = []
        for baimena in baimenak:
            print("Drone zenbakia:",end="")
            print(baimena[2])
            #baimen_drone_id.append(baimena[2])
            droneak.append(self.get_drone_full(baimena[2]))
       

        # for pos,id in enumerate(id_drone):
        #     print(type(id))
        #     drone=self.get_drone_full(id)

        #     if not drone.drone_jabe.erab_id==erab.erab_id:
        #         drone_izen_erakusgarria=drone.drone_izen+"_"+drone.drone_jabe.erab_izen
        #         if baimen[pos] == "Kontrolatu":
        #             drone_izen_erakusgarria=drone.drone_izen + " Kontrolatu"
        #         elif baimen[pos] == "Ikusi":
        #             drone_izen_erakusgarria=drone.drone_izen + " Ikusi"
        #     else:
        #         drone_izen_erakusgarria = drone.drone_izen

        #     droneak.append(drone_izen_erakusgarria)
        
        return droneak
    
    # ===============================================================================================
    # ALDATU: get_erab egin, erabiltzaile ID, izena eta drone zerrenda itzultzen duena
    @multimethod
    def get_erab_full(self: object, izena: str):

        ## ERABILTZAILEA LORTZEKO FUNTZIOA
        #  INPUTS:  Erabiltzailearen izena
        #  OUTPUTS: Erabiltzaile objektu osoa
        
        print("Pew")
        print(izena)
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE Izen = %s", (izena,))
        user = cur.fetchone()
        cur.close()
        if user:
            userprofile = erabiltzailea(user)
        return userprofile if userprofile else None

    @multimethod
    def get_erab_full(self: object, id: int):

        ## ERABILTZAILEA LORTZEKO FUNTZIOA
        #  INPUTS:  Erabiltzailearen IDa
        #  OUTPUTS: Erabiltzaile objektu osoa

        print("Pow")
        print(id)
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE idErabiltzaileak = %s", (id,))
        user = cur.fetchone() 
        cur.close()
        if user:
            userprofile = erabiltzailea(user)
        return userprofile if userprofile else None
    
    def get_erab_baimen(self, erab):
        cur = self.mysql.connection.cursor()
        print(erab.erab_izen)
        print(erab.erab_id)
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (erab.erab_id, ))
        baimenak = cur.fetchall() 
        cur.close()
        return baimenak
    
    def get_drone_baimen(self, drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE idDroneak = %s", (drone.drone_id, ))
        baimenak = cur.fetchall() 
        cur.close()
        return baimenak

    def get_erab_izen(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Izen FROM Erabiltzaileak WHERE idErabiltzaileak = %s", (id_erab,))
        erab_izen = cur.fetchone() 
        cur.close()
        return erab_izen[0]
    
    def get_erab_droneak(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (id_erab,))
        erab_dron = cur.fetchall() 
        cur.close()
        return [sublist[2] for sublist in erab_dron], [sublist[3] for sublist in erab_dron]
    
    # ===============================================================================================
    # ALDAKETAK: Get drone info hurrengoa itzuli behar du: ID, izena, jabea, erabiltzaileak

    @multimethod
    def get_drone_full(self: object, izena: str):

        ## Drone informazioa lortzeko
        #  INPUT:  Dronearen izena
        #  OUTPUT: Drone objektu bat, guztiarekin

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE Izena = %s", (izena,))
        drone = cur.fetchone()
        cur.close()
        if drone:
            sentsoreArray = self.__get_drone_sentsoreak(drone[0])
            jabea = self.get_drone_jabe(drone[0])
            droneprofile = dronea(drone, sentsoreArray, jabea)
        return droneprofile if droneprofile else None

    @multimethod
    def get_drone_full(self: object, droneID: int):

        ## Drone informazioa lortzeko
        #  INPUT:  Dronearen IDa
        #  OUTPUT: Drone objektu bat, guztiarekin

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE idDroneak = %s", (droneID,))
        drone = cur.fetchone()
        cur.close()
        if drone:
            sentsoreArray = self.__get_drone_sentsoreak(drone[0])
            jabea = self.get_drone_jabe(drone[0])
            droneprofile = dronea(drone, sentsoreArray, jabea)
        return droneprofile if droneprofile else None

    @multimethod
    def get_drone_jabe(self:object, id_dron: int):

        ## Drone baten jabea lortzekoQ
        #  INPUT:  Dronearen ID-a
        #  OUTPUT: Erabiltzaile objektu bat, jabearen informazioarekin

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s", (id_dron,"Jabea"))
        jabe_dron = cur.fetchone()
        cur.close()
        return self.get_erab_full(jabe_dron[0])
    
    @multimethod
    def get_drone_jabe(self:object, drone: object):

        ## Drone baten jabea lortzekoQ
        #  INPUT:  Drone objektu bat
        #  OUTPUT: Erabiltzaile objektu bat, jabearen informazioarekin

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s", (drone.drone_id,"Jabea"))
        jabe_dron = cur.fetchone()
        cur.close()
        return self.get_erab_full(jabe_dron[0])
    
    # Oraindik ez dugu erabili hau...?

    def get_drone_erab(self,id_dron):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Droneak_idDroneak = %s", (id_dron,))
        drone_erab = cur.fetchall() 
        cur.close()
        return drone_erab
    
    # ===============================================================================================
    # ALDAKETAK: Erredundantea: Koordenatuak beste eratan funtzionatzea hobe

    def get_drone_mezuak(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Mezuak WHERE Droneak_idDroneak = %s", (id_drone,))
        mezu_drone = cur.fetchall() 
        cur.close()
        return mezu_drone
    
    # Sentsore array bat itzultzen du, drone ID bat hartuz.
    # PRIBATUA
    def __get_drone_sentsoreak(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Drone_Sentsore WHERE Droneak_idDroneak = %s", (id_drone,))
        drone_sentsore_raw = cur.fetchall()
        cur.close()
        drone_sentsore = []
        for sens in drone_sentsore_raw:
            drone_sentsore.append(sentsorea(self.__get_sentsore_info(sens[3])))
        return drone_sentsore
    
    def __get_sentsore_info(self,id_sentsore):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak WHERE idSentsoreak = %s", (id_sentsore,))
        sens_info = cur.fetchone() 
        cur.close()
        return sens_info


    # ===============================================================================================
    # ALDAKETAK: get_drone_sentsore_info hurrengoa itzuliko du: Drone bateko sentsore ID, izena eta azkeneko balio irakurketa

    def get_sentsore_id(self,izena):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak WHERE Izen = %s", (izena,))
        sents = cur.fetchone() 
        cur.close()
        return sents[0]

    def get_drone_sentsore_info(self,id_drone,id_sentsore):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Drone_Sentsore WHERE Droneak_idDroneak = %s AND Sentsoreak_idSentsoreak = %s", (id_drone,id_sentsore))
        dron_sens = cur.fetchone() 
        cur.close()
        return dron_sens
    
    def get_sentsore_balio(self,id_dron_sens):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsore_info WHERE Drone_Sentsore_idDroneSentsore = %s", (id_dron_sens,))
        sens_balio = cur.fetchall() 
        cur.close()
        return sens_balio[-1]
    


    # ===============================================================================================
    # ALDAKETAK: DRONEEN INFORMAZIO GUZTIA BATERA EMAN BEHAR DA
    
    def __getDroneType(self, droneID):
        # Returns an array where the first element is a string that carries the drone type
        cur = self.mysql.connection.cursor()
        query = "SELECT Mota FROM Droneak WHERE idDroneak = {}".format(droneID)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    
    def __getDroneName(self, droneID):
        # Returns an array where the first element is a string that carries the drone name
        cur = self.mysql.connection.cursor()
        query = "SELECT izena FROM Droneak WHERE idDroneak = {}".format(droneID)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_latitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Latitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s " )
        cur.execute(query,(droneID,dir))
        lats = cur.fetchall()
        cur.close()
        return lats
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_longitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s ")
        cur.execute(query,(droneID,dir))
        lons = cur.fetchall()
        cur.close()
        return lons
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_altitudes(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Altitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s " )
        cur.execute(query,(droneID,dir))
        alts = cur.fetchall()
        cur.close()
        return alts
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_timestamps(self, droneID, dir):
        cur = self.mysql.connection.cursor()
        query = ("SELECT Timestamp FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s " )
        cur.execute(query,(droneID,dir))
        times = cur.fetchall()
        cur.close()
        return times
    
    # ===============================================================================================
    # ALDAKETAK: POSIZIOEN INFORMAZIO GUZTIA BATERA EMAN BEHAR DA
    # - Bi funtzio sortuko dira:
    #   - Benetako GPS informazioaren berri ematen duena (Lat, Lng, Alt, Hdg)
    #   - Waypointen berri ematen duena (Lat, Lng, Alt)

    def get_locations_full(self, drone):
        cur = self.mysql.connection.cursor()
        query = "SELECT Latitude, Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s"
        cur.execute(query,(drone.drone_id))
        results = cur.fetchall()
        cur.close()
        return results


    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def getRealLocations(self, droneID):
        # Returns an array of coordinates
        cur = self.mysql.connection.cursor()
        query = "SELECT Latitude, Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s"
        cur.execute(query,(droneID, "DOW"))
        results = cur.fetchall()
        cur.close()
        return results
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def getRealHeadings(self, droneID):
        # Returns an array of floats
        cur = self.mysql.connection.cursor()
        query = "SELECT Heading FROM GPS_kokapena WHERE Droneak_idDroneak = %s AND Noranzkoa = %s"
        cur.execute(query,(droneID, "DOW"))
        results = cur.fetchall()
        cur.close()
        
        cleanresults = []
        for heading in results:
            cleanresults.append(heading[0])

        return cleanresults

    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_waypoints(self, droneID, dir):
        lats = self.get_latitudes(droneID, dir)
        lons = self.get_longitudes(droneID, dir)
        waypoints = []
        if len(lats) == len(lons):
            for i in range(len(lats)):
                waypoints.append([lats[i][0], lons[i][0]])
        return waypoints
    
    # ABSOLUTE DOGSHIT - THIS SHOULD BE THE ONLY FUNCTION HERE
    def get_waypoints_full(self, droneID, dir):
        lats = self.get_latitudes(droneID, dir)
        lons = self.get_longitudes(droneID, dir)
        alts = self.get_altitudes(droneID, dir)
        times = self.get_timestamps(droneID, dir)
        waypoints = []
        if len(lats) == len(lons):
            for i in range(len(lats)):
                waypoints.append([lats[i][0], lons[i][0], alts[i][0], times[i][0]])
        return waypoints

    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_next_waypoint(self, droneID):
        waypoints = self.get_waypoints_full(droneID, "UPF")
        return(waypoints[0])
        
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_waypoint_past(self, droneID):
        waypoints = self.get_waypoints(droneID, "UPP")
        return waypoints

    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_waypoint_future(self, droneID):
        waypoints = self.get_waypoints(droneID, "UPF")
        return waypoints
    
    # ABSOLUTE DOGSHIT - SHOULD BE MANAGED IN CONTROLLER
    def get_all_waypoints(self, droneID):
        pastWaypoints = self.get_waypoint_past(droneID)
        futureWaypoints = self.get_waypoint_future(droneID)

        allWaypoints = []

        for wp in pastWaypoints:
            allWaypoints.append(wp)

        for wp in futureWaypoints:
            allWaypoints.append(wp)
        print("ALL WAYPOINTS")
        print(allWaypoints)
        return(allWaypoints)

    # ===============================================================================================
    # Ez da datu basea baina hemen ondo dagoela esango nuke. Mota hobe kudeatzeko erarik ote dago?

    def get_banned_areas(self, droneType):
        if droneType.lower() == "plane":
            return(bans.planeBans)
        elif droneType.lower() == "helicopter":
            return(bans.planeBans)
    
    def get_restricted_areas(self, droneType):
        if droneType.lower() == "plane":
            return(bans.planeLimits)
        elif droneType.lower() == "helicopter":
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

    def insert_GPS_kokapena(self,id_drone,lng,ltd,alt,hdg,timestamp,noranzkoa):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO GPS_kokapena (Droneak_idDroneak,Longitude,Latitude,Altitude,Heading,Timestamp,Noranzkoa) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(id_drone,lng,ltd,alt,hdg,timestamp,noranzkoa))
        self.mysql.connection.commit()
        cur.close()

    def insert_Mezuak(self,id_drone,edukia,timestamp,noranzkoa):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Mezuak (Droneak_idDroneak,Eduikia,Timestamp,Noranzkoa) VALUES (%s,%s,%s,%s)"
        cur.execute(query,(id_drone,edukia,timestamp,noranzkoa))
        self.mysql.connection.commit()
        cur.close()

    def insert_Partekatzeak(self,erabiltzaile,id_drone,baimena):
        print("PARTEKATZEKO DATUAK:")
        print(erabiltzaile.erab_id)
        print(id_drone.drone_id)
        print(baimena)
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Partekatzeak (Erabiltzaileak_idErabiltzaileak,Droneak_idDroneak,Baimenak_idBaimenak) VALUES (%s,%s,%s)"
        cur.execute(query,(erabiltzaile.erab_id,id_drone.drone_id,baimena))
        self.mysql.connection.commit()
        cur.close()

    def insert_Sentsore_info(self,id_drone_sents,balioa,timestamp):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Sentsore_info (Dronea_Sentsore_idDroneSentsore,Balioa,Timestamp) VALUES (%s,%s,%s)"
        cur.execute(query,(id_drone_sents,balioa,timestamp))
        self.mysql.connection.commit()
        cur.close()

    def insert_Sentsoreak(self,izena,mota,deskribapena):
        try:
            cur = self.mysql.connection.cursor()
            query = "INSERT INTO Sentsoreak (Izena,Mota,Deskribapena) VALUES (%s,%s,%s)"
            cur.execute(query,(izena,mota,deskribapena))
            self.mysql.connection.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            cur.close()
    
    def update_Droneak(self,izena,mota,deskribapena,id):
        cur = self.mysql.connection.cursor()
        query = "UPDATE Droneak SET Izena=%s, Mota=%s, Deskribapena=%s WHERE idDroneak=%s"
        cur.execute(query,(izena,mota,deskribapena,id))
        self.mysql.connection.commit()
        cur.close()
        
