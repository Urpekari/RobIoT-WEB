import requests
import random
import time

idealLat = 43.354896
idealLon = -3.141321

gwid = 2

url = "http://localhost:5000/gwInsert/{}".format(gwid)

while True:
    data = {

        "gwid":gwid,
        "robiotId":1,
        "lat":random.uniform(idealLat-0.002, idealLat+0.002),
        "lon":random.uniform(idealLon-0.002, idealLon+0.002),
        "alt":random.uniform(15,25),
        "hdg":random.uniform(0,360),
    }

    response = requests.post(url, json=data)
    print(response.json())
    time.sleep(1)