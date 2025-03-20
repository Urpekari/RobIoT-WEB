
import env

class tables():
    Baimenak="Baimenak"
    Droneak="Droneak"
    Drone_Sentsore="Drone_sentsore"
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
    
    # Maparekin erabiltzeko atalak

    def getRealLocations(self, droneID):
        cur = self.mysql.connection.cursor()
        query = "SELECT Latitude, Longitude FROM GPS_kokapena WHERE Droneak_idDroneak = {}".format(droneID)
        cur.execute(query)
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

class input():
    _instance = None

    def __init__(self,mysql):
        self.mysql=mysql

    def insert_Droneak(self,data):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Droneak (Izena,Mota,Deskribapena) VALUES (%s,%s,%s)"
        cur.execute(query,(data[0],data[1],data[2]))
        self.mysql.connection.commit()
        cur.close()

    def insert_Drone_Sentsore(self,data):
        cur = self.mysql.connection.cursor()
        query = "INSERT INTO Droneak (Ezizena,Droneak_idDroneak,Sentsoreak_idSentsoreak) VALUES (%s,%d,%d)"
        cur.execute(query,(data[0],data[1],data[2]))
        self.mysql.connection.commit()
        cur.close()

    def datuak_sartu(self,izena, abizena, pasahitza, email, dokumentuak):
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