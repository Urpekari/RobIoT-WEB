# RobIoT-WEB
LoRa-based general purpose control system

## Initial setup
An env.py file must be provided in the root directory.
That file must contain the following fields:
```py
mysql_host_ip = '[host]'                            #(default: localhost)
mysql_username = '[username in plaintext]'          #(default: root)
mysql_password = '[password in plaintext]'          #(default: root)
mysql_db_name = '[database name in plaintext]'      #(default: robiot)
```
The default credentials are **NO GOOD FOR A LARGE DEPLOYMENT**

## Launch via cli:
**Debug:**
python -m flask run

**Demo deployment:**
python -m flask run --host=[Host IPv4 Address] --port=[TCP port]

python -m flask run --host=0.0.0.0 *This will make the server available on EVERY IP INTERFACE*
