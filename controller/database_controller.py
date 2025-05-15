import other.banned_areas as bans
from multimethod import *
from app import *

from model.SQL_functions import output, input

from model.gpspoint import gpspoint
from model.drone_osoa import drone_osoa

from model.drone_sentsore import drone_sentsore
from model.droneak import droneak
from model.erabiltzaileak import erabiltzaileak
from model.gps_kokapena import gps_kokapena
from model.mezuak import mezuak
from model.partekatzeak import partekatzeak
from model.sentsore_info import sentsore_info
from model.sentsoreak import sentsoreak

# Klase bat badago datuak gordetzen dituena, klasea bidaltzea lehenetsiko dugu
# Adibidez, droneID edo erabiltzaile izena bidali nahi izatekotan, drone klaseko objektu bat eta erabiltzailea klaseko objektuak lehenetsiko ditugu

class database_controller():

    def __init__(self,mysql):
        self.mysql=mysql
        self.dboutput=output(mysql)
        self.dbinput=input(mysql)

    #def create_dowload_file(self,...):

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

#######################################################################
# TAULAK LORTZEKO FUNTZIOAK
#######################################################################

    def get_Baimenak_table (self):
        baimenak = self.dboutput.get_whole_table("Baimenak")
        return baimenak

    def get_Drone_Sentsore_table (self):
        drone_sentsore_raw = self.dboutput.get_whole_table("Drone_Sentsore")
        drone_sentsore_list = []
        for dron_sents in drone_sentsore_raw:
            drone = self.dboutput.find_droneak(dron_sents[2])
            sentsore = self.dboutput.find_sentsoreak(dron_sents[3])
            drone_sentsore_list.append(drone_sentsore(dron_sents,droneak(drone),sentsoreak(sentsore)))

        return drone_sentsore_list
    
    def get_Droneak_table (self):
        droneak_raw = self.dboutput.get_whole_table("Droneak")
        droneak_list = []
        for dron in droneak_raw:
            droneak_list.append(droneak(dron))

        return droneak_list
    
    def get_Erabiltzaileak_table (self):
        erabiltzaileak_raw = self.dboutput.get_whole_table("Erabiltzaileak")
        erabiltzaileak_list = []
        for erab in erabiltzaileak_raw:
            erabiltzaileak_list.append(erabiltzaileak(erab))

        return erabiltzaileak_list
    
    def get_GPS_kokapena_table (self):
        gps_kokapena_raw = self.dboutput.get_whole_table("GPS_kokapena")
        gps_kokapena_list = []
        for gps_kokap in gps_kokapena_raw:
            drone = self.dboutput.find_droneak(gps_kokap[1])
            gps_kokapena_list.append(gps_kokapena(gps_kokap,droneak(drone)))
        
        return gps_kokapena_list
    
    def get_Mezuak_table (self):
        mezuak_raw = self.dboutput.get_whole_table("Mezuak")
        mezuak_list = []
        for mezu in mezuak_raw:
            drone = self.dboutput.find_droneak(mezu[1])
            mezuak_list.append(mezuak(mezu,droneak(drone)))

        return mezuak_list
    
    def get_Partekatzeak_table (self):
        partekatzeak_raw = self.dboutput.get_whole_table("Partekatzeak")
        partekatzeak_list = []
        for partekatze in partekatzeak_raw:
            erab = self.dboutput.find_droneak(partekatze[1])
            drone = self.dboutput.find_droneak(partekatze[2])
            partekatzeak_list.append(partekatzeak(partekatze,erabiltzaileak(erab),droneak(drone)))
        
        return partekatzeak_list
    
    def get_Sentsore_info_table (self):
        sentsore_info_raw = self.dboutput.get_whole_table("Sentsore_info")
        sentsore_info_list = []
        for sents_info in sentsore_info_raw:
            drone = self.dboutput.find_droneak(sents_info[1])
            sentsore_info_list.append(sentsore_info(sents_info,droneak(drone)))
        
        return sentsore_info_list
    
    def get_Sentsoreak_table (self):
        sentsoreak_raw = self.dboutput.get_whole_table("Sentsoreak")
        sentsoreak_list = []
        for sentsore in sentsoreak_raw:
            sentsoreak_list.append(sentsoreak(sentsore))
        
        return sentsoreak_list

#######################################################################
# BILAKETA FUNTZIOAK
#######################################################################

    @multimethod
    def lortu_erabiltzailea(self, erab_id):
        user_raw = self.dboutput.find_erabiltzaileak(erab_id)
        user = erabiltzaileak(user_raw)
        return user
    
    @multimethod
    def lortu_erabiltzailea(self, erab_name):
        user_raw = self.dboutput.find_erab_w_name(erab_name)
        user = erabiltzaileak(user_raw)
        return user
    
    def lortu_dronea(self, drone_id):
        drone_raw = self.dboutput.find_droneak(drone_id)
        drone = droneak(drone_raw)
        return drone
    
    def lortu_sentsorea(self, sents_id):
        sentsore_raw = self.dboutput.find_sentsoreak(sents_id)
        sentsore = sentsoreak(sentsore_raw)
        return sentsore
    
    def lortu_erabiltzailearen_droneak(self, erab_id):
        partekatze_list_raw = self.dboutput.find_partekatzeak_w_erab(erab_id)
        partekatze_list = []
        for partekatze in partekatze_list_raw:
            drone = self.dboutput.find_droneak(partekatze[2])
            jabe = self.dboutput.find_drone_jabe_w_drone(drone[0])
            erab = self.dboutput.find_erabiltzaileak(jabe[1])
            partekatze_list.append(partekatzeak(partekatze,erabiltzaileak(erab),droneak(drone)))
        
        return partekatze_list
    
    def lortu_drone_info_osoa(self, drone_id):
        if drone_id and isinstance(drone_id, (int)):
            try:
                drone_raw = self.dboutput.find_droneak(drone_id)
                
                if not drone_raw:
                    return(-1)
                
                drone = droneak(drone_raw)
                sentsore_list_raw = self.dboutput.find_dron_sents_w_drone(drone_id)
                sentsore_list = []
                for sents in sentsore_list_raw:
                    sentsore = self.dboutput.find_sentsoreak(sents[3])
                    sentsore_list.append(sentsoreak(sentsore))

                erab_list_raw = self.dboutput.find_partekatzeak_w_drone(drone_id)
                jabe = None
                kontrol_list = []
                ikus_list = []
                for erab in erab_list_raw:
                    erabiltzaile = self.dboutput.find_erabiltzaileak(erab[1])
                    if erab[3] == "Jabea":
                        jabe = erabiltzaileak(erabiltzaile)

                    elif erab[3] == "Kontrolatu":
                        kontrol_list.append(erabiltzaileak(erabiltzaile))

                    elif erab[3] == "Ikusi":
                        ikus_list.append(erabiltzaileak(erabiltzaile))
                
                drone_info_osoa = drone_osoa(drone,sentsore_list,jabe,kontrol_list,ikus_list)
                if drone_info_osoa:
                    print(drone_info_osoa)
                    return drone_info_osoa
                else:
                    return -1
            
            except:
                return(-1)
        else:
            return(-1)
    
    def lortu_drone_GPS_informazioa(self, drone_id):
        gps_list_raw = self.dboutput.find_GPS_kokapen_w_drone(drone_id)
        gps_list = []
        for gps in gps_list_raw:
            gps_list.append(gpspoint(gps))

        return gps_list
    
    def lortu_hurrengo_jauzia(self, drone_id):
        gps_list_raw = self.dboutput.find_GPS_kokapen_w_drone(drone_id)
        hurr_jauz = None
        for gps in gps_list_raw:
            if gps[7] == "UPF":
                hurr_jauz = gpspoint(gps)
                break
        
        return hurr_jauz

    def lortu_azalerak (self, droneType):
        banned = self.dboutput.get_banned_areas(droneType)
        resticted = self.dboutput.get_restricted_areas(droneType)
        return banned, resticted


#######################################################################
# ERABILTZAILEA BILATZEKO IZEN + PASS
#######################################################################

    def erabiltzailea_egiaztatu(self,username, password):
        user_raw = self.dboutput.find_erab_w_name_n_pass(username, password)
        if user_raw:
            user = erabiltzaileak(user_raw)
            return user,True
        
        else:
            return None,False

#######################################################################
# DATU BASERA SARTZEKO FUNTZIOAK
#######################################################################

    def sartu_erabiltzaile_berria(self, izena, abizena, pasahitza, email, dokumentuak):
        return self.dbinput.insert_Erabiltzaileak(izena, abizena, pasahitza, email, dokumentuak)
    
    def sartu_drone_berria(self, izena, mota, deskribapena, erab_id):
        self.dbinput.insert_Droneak(izena, mota, deskribapena)
        dron = self.dboutput.find_drone_w_izen_mota_desk(izena, mota, deskribapena)
        self.dbinput.insert_Partekatzeak(erab_id,dron[0],"Jabea")
    
    def sartu_sentsore_berria(self, izena, mota, deskribapena):
        return self.dbinput.insert_Sentsoreak(izena, mota, deskribapena)
    
    def sartu_ibilbide_berria(self, id_drone, koord_list, alt, head, timestmp):
        for koord in koord_list:
            self.dbinput.insert_GPS_kokapena(id_drone, koord[1], koord[0], alt, head, timestmp, "UPF")

    def sartu_momentuko_kokapena(self, drone_id, long, lat, alt, head, timestmp):
        self.dbinput.insert_GPS_kokapena(drone_id, long, lat, alt, head, timestmp, "DOW")

    def eguneratu_heldutako_waypoint(self, gps_id):
        self.dbinput.update_GPS_kokapena(gps_id)
    
    def dronea_partekatu(self, drone_id, erab_name, baimen):
        erab = self.dboutput.find_erab_w_name(erab_name)
        if erab:
            self.dbinput.insert_Partekatzeak(erab[0],drone_id,baimen)
            return True
        
        else:
            return False
    
    def sentsoreak_esleitu(self, drone_id, sents_list):
        for sents in sents_list:
            self.dbinput.insert_Drone_Sentsore("", drone_id, int(sents))
    
    def aldatu_dronea(self, izena, mota, deskribapena, drone_id):
        self.dbinput.update_Droneak(izena, mota, deskribapena, drone_id)