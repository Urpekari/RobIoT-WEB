import requests
import random
import time

idealLat = 43.354896
idealLon = -3.141321

gwid = 2

url = "http://127.0.0.1:5000/gwInsert/{}".format(gwid)

while True:
    data = {

        "gwid":gwid,
        "robiotId":2,
        "lat":random.uniform(idealLat-0.002, idealLat+0.002),
        "lon":random.uniform(idealLon-0.002, idealLon+0.002),
        "alt":random.uniform(15,25),
    }

    response = requests.post(url, json=data)
    print(response.json())
    time.sleep(1)