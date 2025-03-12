BaimenMotak="baimenmotak"
Droneak="droneak"
DroneSentsore="dronesentsoreak"
Erabiltzaileak="erabiltzaileak"
Mezuak="mezuak"
Partekatzeak="partekatzeak"
Posizioak="posizioak"
Sentsoreak="sentsoreak"
SentsoreInfo="sentsoreinfo"

BaimenMotak_header=["ID"]
Droneak_header=["ID","Mota"]
DroneSentsore_header=["ID","Drone","Sentsore"]
Erabiltzaileak_header=["ID","Izena","Abizenak","Legezko dokumentuak","Pasahitza"]
Mezuak_header=["ID","Drone","Timestamp","Edukia"]
Partekatzeak_header=["ID","Erabiltzailea","Baimen mota","Drone"]
Posizioak_header=["ID","Drone","Timestamp","Longitude","Latitude"]
Sentsoreak_header=["ID"]
SentsoreInfo_header=["ID","Drone sentsore erlazioa","Timestamp","Balioa"]

def get_headers(mysql,name):
    cur = mysql.connection.cursor()
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = {0}".format(name)
    cur.execute(query)
    results = cur.fetchall()
    return results

def get_info(mysql,name):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM {0}".format(name)
    cur.execute(query)
    results = cur.fetchall()
    return results

def create_csv(mysql,name):
    csv_array=[]
    array=get_info(mysql,name)
    for row in array:
        for column in row:
            csv_array.append(str(column))
            csv_array.append(';')
        csv_array=csv_array[:-1]
        csv_array.append('\n')
    return csv_array