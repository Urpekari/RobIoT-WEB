
class tables():
    Baimenak="baimenak"
    Droneak="droneak"
    Drone_Sentsore="drone_sentsore"
    Erabiltzaileak="erabiltzaileak"
    Mezuak="mezuak"
    Partekatzeak="partekatzeak"
    GPS_kokapena="gps_kokapena"
    Sentsoreak="sentsoreak"
    Sentsore_info="sentsore_info"

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
        cur.execute("SELECT * FROM erabiltzaileak WHERE Izen = %s AND Pasahitza = %s", (username, password))
        usuario = cur.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
        cur.close()
        if usuario is None:
            return 0
        else:
            return 1

class input():

    def __init__(self,mysql):
        self.mysql=mysql

    def insert_Droneak(mysql,data):
        cur = mysql.connection.cursor()
        query = "INSERT INTO droneak (Izena,Mota,Deskribapena) VALUES (%s,%s,%s)"
        cur.execute(query,(data[0],data[1],data[2]))
        mysql.connection.commit()
        cur.close()

    def insert_Drone_Sentsore(mysql,data):
        cur = mysql.connection.cursor()
        query = "INSERT INTO droneak (Ezizena,Droneak_idDroneak,Sentsoreak_idSentsoreak) VALUES (%s,%d,%d)"
        cur.execute(query,(data[0],data[1],data[2]))
        mysql.connection.commit()
        cur.close()