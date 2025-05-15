import other.banned_areas as bans
from multimethod import *
from app import *

# Klase bat badago datuak gordetzen dituena, klasea bidaltzea lehenetsiko dugu
# Adibidez, droneID edo erabiltzaile izena bidali nahi izatekotan, drone klaseko objektu bat eta erabiltzailea klaseko objektuak lehenetsiko ditugu

class output():
    _instance = None

    def __init__(self,mysql):
        self.mysql=mysql

#######################################################################
# TAULAK LORTZEKO FUNTZIOA
#######################################################################

    def get_whole_table(self,table_name):
        cur = self.mysql.connection.cursor()
        query = "SELECT * FROM {0}".format(table_name)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results

#######################################################################
# ID DITARTEKO BILAKETAK
#######################################################################
    
    def find_drone_sentrore(self,id_dron_sents):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Drone_Sentsore WHERE idDroneSentsore = %s", (id_dron_sents,))
        drone_sentsore = cur.fetchone()
        cur.close()
        return drone_sentsore
    
    def find_droneak(self,id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE idDroneak = %s", (id_drone,))
        drone = cur.fetchone()
        cur.close()
        return drone
    
    def find_erabiltzaileak(self,id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE idErabiltzaileak = %s", (id_erab,))
        erab = cur.fetchone()
        cur.close()
        return erab
    
    def find_gps_kokapena(self,id_gpsKokap):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM GPS_kokapena WHERE idGPS_kokapena = %s", (id_gpsKokap,))
        gpsKokap = cur.fetchone()
        cur.close()
        return gpsKokap
    
    def find_mezuak(self,id_mezuak):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Mezuak WHERE idMezuak = %s", (id_mezuak,))
        mezu = cur.fetchone()
        cur.close()
        return mezu
    
    def find_partekatzeak(self,id_partekatze):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE idPartekatzeak = %s", (id_partekatze,))
        part = cur.fetchone()
        cur.close()
        return part
    
    def find_sentsore_info(self,id_sentsInfo):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsore_info WHERE idSentsore_info = %s", (id_sentsInfo,))
        sentsInfo = cur.fetchone()
        cur.close()
        return sentsInfo
    
    def find_sentsoreak(self,id_sents):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Sentsoreak WHERE idSentsoreak = %s", (id_sents,))
        sents = cur.fetchone()
        cur.close()
        return sents

#######################################################################
# BILAKETA GEHIGARRIAK
#######################################################################
    
    def find_erab_w_name(self, name):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE Izen = %s", (name,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def find_erab_w_name_n_pass(self, username, password):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Erabiltzaileak WHERE Izen = %s AND Pasahitza = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        return user
    
    def find_dron_sents_w_drone(self, id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Drone_Sentsore WHERE Droneak_idDroneak = %s", (id_drone,))
        drone_sentsore = cur.fetchall()
        cur.close()
        return drone_sentsore
    
    def find_drone_w_izen_mota_desk(self, izen, mota, desk):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Droneak WHERE Izena=%s AND Mota=%s AND Deskribapena=%s", (izen, mota, desk))
        user = cur.fetchall()
        cur.close()
        return user[-1]
    
    def find_partekatzeak_w_drone(self, id_drone):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Droneak_idDroneak = %s", (id_drone,))
        partekatze = cur.fetchall()
        cur.close()
        return partekatze
    
    def find_partekatzeak_w_erab(self, id_erab):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM Partekatzeak WHERE Erabiltzaileak_idErabiltzaileak = %s", (id_erab,))
        partekatze = cur.fetchall()
        cur.close()
        return partekatze
    
    def find_GPS_kokapen_w_drone(self, id_drone):
        cur = self.mysql.connection.cursor()
        query = ("SELECT * FROM GPS_kokapena WHERE Droneak_idDroneak = %s")
        cur.execute(query,(id_drone,))
        gps = cur.fetchall()
        cur.close()
        return gps
    
    def find_drone_jabe_w_drone(self, id_drone):
        cur = self.mysql.connection.cursor()
        query = ("SELECT * FROM Partekatzeak WHERE Droneak_idDroneak = %s AND Baimenak_idBaimenak = %s")
        cur.execute(query,(id_drone,"Jabea"))
        jabe = cur.fetchone()
        cur.close()
        return jabe
    
#######################################################################
# MAPA BETETZEKO INFORMAZIOA
#######################################################################

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
        

#######################################################################
#######################################################################
#######################################################################

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

    def update_GPS_kokapena(self,gps_id):
        cur = self.mysql.connection.cursor()
        query = "UPDATE GPS_kokapena SET Noranzkoa = %s WHERE idGPS_kokapena = %s"
        print(f"Executing query: {query} with params: {('UPP', gps_id)}")
        cur.execute(query,("UPP", gps_id))
        self.mysql.connection.commit()
        cur.close()

    def insert_Mezuak(self,id_drone,edukia,timestamp,noranzkoa):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Mezuak (Droneak_idDroneak,Eduikia,Timestamp,Noranzkoa) VALUES (%s,%s,%s,%s)"
        cur.execute(query,(id_drone,edukia,timestamp,noranzkoa))
        self.mysql.connection.commit()
        cur.close()

    def insert_Partekatzeak(self, erab_id, drone_id, baimena):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Partekatzeak (Erabiltzaileak_idErabiltzaileak,Droneak_idDroneak,Baimenak_idBaimenak) VALUES (%s,%s,%s)"
        cur.execute(query,(erab_id, drone_id, baimena))
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