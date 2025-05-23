# RobIoT-WEB
LoRa-based general purpose drone control system.

Urpekari Proiektua - 2025

## Requirements and dependencies:
- A SQL database (RobIoT has been tested and proven to be working with Oracle MySQL and MariaDB)
- Python 3.12.3 or higher
- The following Pip packages:
  - blinker            1.9.0
  - branca             0.8.1
  - certifi            2025.1.31
  - charset-normalizer 3.4.1
  - click              8.1.8
  - Flask              3.1.0
  - flask-cors         5.0.1
  - Flask-MySQLdb      2.0.0
  - folium             0.19.5
  - haversine          2.9.0
  - idna               3.10
  - iniconfig          2.1.0
  - itsdangerous       2.2.0
  - Jinja2             3.1.6
  - MarkupSafe         3.0.2
  - multimethod        2.0
  - mysqlclient        2.2.7
  - numpy              2.2.3
  - overpy             0.7
  - packaging          25.0
  - pip                25.1
  - pluggy             1.6.0
  - pytest             8.3.5
  - requests           2.32.3
  - urllib3            2.3.0
  - Werkzeug           3.1.3
  - xyzservices        2025.1.0

## Initial setup
An env.py file must be provided in the root directory.
That file must contain the following fields:
```py
mysql_host_ip = '[host]'                            #(default: localhost)
mysql_username = '[username in plaintext]'          #(default: root)
mysql_password = '[password in plaintext]'          #(default: root)
mysql_db_name = '[database name in plaintext]'      #(default: robiot)
```
The default credentials are **NO-GOOD FOR A LARGE DEPLOYMENT**

## Required per-deployment changes:
*(This should be enhanced and automated in a future release)*

- Adjust the IP addresses/URLs of any scripts to match your exact deployment in the following files:
  - mapUpdate.js

## Launching via cli:
*Remember to use the correct virtual environment!*

**Debug:**
python -m flask --debug run

**Demo deployment:**
python -m flask run --host=[Host IPv4 Address] --port=[TCP port]

python -m flask run --host=0.0.0.0 *This will make the server available on EVERY IP INTERFACE*
