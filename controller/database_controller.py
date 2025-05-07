import other.banned_areas as bans
from multimethod import *
from app import *

from model.erabiltzailea import erabiltzailea
from model.partekatzea import partekatzea
from model.sentsorea import sentsorea
from model.gpspoint import gpspoint
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
        baimenak=self.__get_erab_baimen(erab)
        #baimen_drone_id = []
        droneak = []
        for baimena in baimenak:
            print("Drone zenbakia:",end="")
            print(baimena[2])
            #baimen_drone_id.append(baimena[2])
            droneak.append(self.get_drone_full(baimena[2]))
        
        return droneak
    
    # ===============================================================================================
    # ALDATU: get_erab egin, erabiltzaile ID, izena eta drone zerrenda itzultzen duena
    @multimethod
    def get_erab_full(self: object, izena: str):

        ## ERABILTZAILEA LORTZEKO FUNTZIOA
        #  INPUTS:  Erabiltzailearen izena
        #  OUTPUTS: Erabiltzaile objektu osoa
        
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

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE idErabiltzaileak = %s", (id,))
        user = cur.fetchone() 
        cur.close()
        if user:
            userprofile = erabiltzailea(user)
        return userprofile if userprofile else None
    
    def __get_erab_baimen(self, erab):
        cur = self.mysql.connection.cursor()
        print(erab.erab_izen)
        print(erab.erab_id)
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (erab.erab_id, ))
        baimenak = cur.fetchall() 
        cur.close()
        return baimenak
    
    def __get_drone_baimen(self, drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE idDroneak = %s", (drone.drone_id, ))
        baimenak = cur.fetchall() 
        cur.close()
        return baimenak
    
    # Hau non erabiltzen den bilatu eta kendu
    def get_erab_droneak(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (id_erab,))
        erab_dron = cur.fetchall() 
        cur.close()
        return [sublist[2] for sublist in erab_dron], [sublist[3] for sublist in erab_dron]
    
    @multimethod
    def get_partekatze_full_erabiltzaileArabera(self: object, erab:object):
        print("GET PARTEKATZE FULL ERABILTZAILEAREN ARABERA:!")
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (erab.erab_id,))
        erab_dron = cur.fetchall()
        print(erab_dron)
        cur.close()
        partekatzeak = []
        for partek in erab_dron:
            partekatzeak.append(partekatzea(partek, self.get_erab_full(partek[1]), self.get_drone_full(partek[2])))
        return(partekatzeak)

    @multimethod
    def get_partekatze_full_erabiltzaileArabera(self: object, id_erab:int):
        print("GET PARTEKATZE FULL ERABILTZAILEAREN ARABERA:!")
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (id_erab,))
        erab_dron = cur.fetchall()
        print(erab_dron)
        cur.close()
        partekatzeak = []
        for partek in erab_dron:
            partekatzeak.append(partekatzea(partek, self.get_erab_full(partek[1]), self.get_drone_full(partek[2])))
        return(partekatzeak)
    
    @multimethod
    def get_partekatze_full_droneArabera(self: object, id_drone: int):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Droneak_idDroneak = %s", (id_drone,))
        erab_dron = cur.fetchall()
        cur.close()
        partekatzeak = []
        for partek in erab_dron:
            partekatzeak.append(partekatzea(partek, self.get_erab_full(partek[1]), self.get_drone_full(partek[2])))
        return(partekatzeak)
    
    @multimethod
    def get_partekatze_full_droneArabera(self: object, drone: object):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Droneak_idDroneak = %s", (drone.drone_id,))
        erab_dron = cur.fetchall()
        cur.close()
        partekatzeak = []
        for partek in erab_dron:
            partekatzeak.append(partekatzea(partek, self.get_erab_full(partek[1]), self.get_drone_full(partek[2])))
        return(partekatzeak)
    
    ## Baimen onargarri guztien zerrenda
    # INPUT: Ezer
    # OUTPIT: Baimen array bat
    def get_baimen_posible_zerrenda(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Baimenak")
        baimenak = cur.fetchall()
        cur.close()
        return(baimenak)



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
            kontroladoreak = self.__get_drone_kontrol(drone[0])
            ikusleak = self.__get_drone_ikusle(drone[0])
            droneprofile = dronea(drone, sentsoreArray, jabea, kontroladoreak, ikusleak)
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
            kontroladoreak = self.__get_drone_kontrol(drone[0])
            ikusleak = self.__get_drone_ikusle(drone[0])
            droneprofile = dronea(drone, sentsoreArray, jabea, kontroladoreak, ikusleak)
        return droneprofile if droneprofile else None

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

    @multimethod
    def get_drone_jabe(self:object, id_dron: int):

        ## Drone baten jabea lortzeko
        #  INPUT:  Dronearen ID-a
        #  OUTPUT: Erabiltzaile objektu bat, jabearen informazioarekin

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s", (id_dron,"Jabea"))
        jabe_dron = cur.fetchone()
        cur.close()
        if jabe_dron:
            return self.get_erab_full(jabe_dron[0])
        else:
            return None

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
    
    ## Drone baten kontrola duten erabiltzaileen ID-ak lortzeko
    # INPUT:  Drone id bat
    # OUTPUT: Erabiltzaile id array bat    
    def __get_drone_kontrol(self,id_dron):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND (Baimenak_idBaimenak = %s OR Baimenak_idBaimenak = %s)", (id_dron, "Jabea", "Kontrolatu"))
        drone_kontrol = cur.fetchall()
        drone_kontroladoreak = []
        for kontroladoreId in drone_kontrol:
            drone_kontroladoreak.append(kontroladoreId[0])
        cur.close()
        return drone_kontroladoreak
    
    ## Drone baten kontrola EZ duten baina ikus dezaketeen erabiltzaileen ID-ak lortzeko
    # INPUT:  Drone id bat
    # OUTPUT: Erabiltzaile id array bat    
    def __get_drone_ikusle(self,id_dron):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT Erabiltzaileak_idErabiltzaileak FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s", (id_dron, "Ikusi"))
        drone_ikusle = cur.fetchall()
        drone_ikusleak = []
        for ikusleId in drone_ikusle:
            drone_ikusleak.append(ikusleId[0])
        cur.close()
        return drone_ikusleak
    
    # ===============================================================================================
    # ALDAKETAK: Erredundantea: Koordenatuak beste eratan funtzionatzea hobe

    def get_drone_mezuak(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Mezuak WHERE Droneak_idDroneak = %s", (id_drone,))
        mezu_drone = cur.fetchall() 
        cur.close()
        return mezu_drone
    
    ## Sentsoreen informaziioa lortzeko
    # Input:  Drone id bat
    # Output: Sentsore objektu array bat
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

    # Sentsore ID bat erabiliz sentsore objektua lortzeko
    # INPUT: Sentsore ID
    # OUTPUT: Sentsore Objektua

    def get_sentsore_full(self, sens_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak WHERE idSentsore_info = %s", (sens_id,))
        sens_info = cur.fetchone()
        cur.close()
        sentsore_osoa = (sentsorea(sens_info))
        return sentsore_osoa

    def get_sentsore_guztiak(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak")
        sens_info = cur.fetchall()
        cur.close()
        sentsore_osoak = []
        for sens in sens_info:
            sentsore_osoak.append(sentsorea(sens))
        return sentsore_osoak

    # ===============================================================================================
    # ALDAKETAK: get_drone_sentsore_info hurrengoa itzuliko du: Drone bateko sentsore ID, izena eta azkeneko balio irakurketa

    def __get_sentsore_id(self,izena):
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
    
    def get_gps_full(self, drone):

        ## GPS datuak osotasunean lortzeko, drone baterako
        # INPUT: Drone objektu bat
        # OUTPUT: gpspoint objektuen array bat

        cur = self.mysql.connection.cursor()
        query = ("SELECT * FROM GPS_kokapena WHERE Droneak_idDroneak = %s")
        cur.execute(query,(drone.drone_id,))
        gps_raw = cur.fetchall()
        cur.close()
        gpsProfiles = []
        print("GPS RAW POINT:")
        print(gps_raw)
        for gps_raw_point in gps_raw:
            gpsProfiles.append(gpspoint(gps_raw_point))
        return(gpsProfiles)

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

    def insert_Drone_Sentsore(self:object,ezizen:str,id_drone:int,id_sents:int):
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


    # # TODO: KONPONDU
    def insert_Partekatzeak(self, erabiltzailea, dronea, baimena):
        print("Erabiltzailea:")
        print(erabiltzailea.erab_izen)
        print("Dronea:")
        print(dronea.drone_izen)
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Partekatzeak (Erabiltzaileak_idErabiltzaileak,Droneak_idDroneak,Baimenak_idBaimenak) VALUES (%s,%s,%s)"
        print(query)
        cur.execute(query,(erabiltzailea.erab_id, dronea.drone_id, baimena))
        self.mysql.connection.commit()
        cur.close()
        return("Done!")


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
        
