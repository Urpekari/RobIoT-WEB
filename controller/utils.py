import tkinter as tk
import haversine as hs
from haversine import Unit


# GPS puntu biren arteko distantzia kalkulatzen du.
# Haversine funtzioa ez da oso zehatza poloen inguruan.
def getGPSDistance(currentCoords, compareCoords):
    return(hs.haversine(currentCoords, compareCoords, unit=Unit.METERS))

# Waypoint zerrenda bat hartzen du eta ibilbide osoaren distantziarekin erantzuten du
def getFullPathDistance(gpsPathWPs):
    # print(gpsPathWPs)
    if(gpsPathWPs != None):
        fulldistance = 0
        for i in range(len(gpsPathWPs)-1):
            # print(fulldistance)
            fulldistance = fulldistance + getGPSDistance(gpsPathWPs[i], gpsPathWPs[i + 1])
        return(fulldistance)
    else:
        return None

# GPS puntuen arteko abiadura kalkulatzen du. Denbora tartea eman behar zaio.
# GPS gailuek eta beste sentsoreek ere kalkulatu dezakete.
# Waypointen arteko abiadura lortzeko ere erabili daiteke, hau da, pasatutako waypointak erabiliz eta ez GPS-ko laginak.
def getSpeed(currentCoords, compareCoords, deltaT):

    return(getGPSDistance(currentCoords, compareCoords)/deltaT)

# Estimated Time of Arrival kalkulatzeko
def getEta(distance, speed):
    if(distance != None and speed!= None):
        return(distance/speed)
    else:
        return(0)