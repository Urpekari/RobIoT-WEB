from flask import Flask, request, render_template, redirect, url_for, session #Importa Flask y sus funciones principales para crear la aplicación web
import mysql.connector  # Si usamos MySQL


app = Flask(__name__)
app.secret_key = 'pasahitza'

#ME FALTA POR CAMBIAR LODEL SQLITE POR MYSQL

def erabiltzailea_egiaztatu(username, password): 
    conn = sqlite3.connect('my.db') #sortu konexioa datu basearekin my.db, sqlitearen izena
    cursor = conn.cursor() # Crea un cursor, que es un objeto que permite ejecutar consultas SQL en la base de datos.
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone() #Obtiene el primer resultado de la consulta y lo guarda en usuario.
    conn.close()
    return usuario

@app.route('/')
def login():
    return render_template('login.html') #Este código indica que cuando un usuario accede a la ruta /, Flask devuelve la página login.html.

@app.route('/auth', methods=['POST'])
def auth(): #define la funcion auth que se ejecuta cuando el usuario intenta iniciar sesion (esta en el html puesto)
    username = request.form['username'] #flask obtiene el usuario y contraseña enviados desde el form del html
    password = request.form['password']
    
    if erabiltzailea_egiaztatu(username, password): #llama a la funcion de arriba q mira en la base de datos
        session['usuario'] = username #guarda el usuario en session que es como una memoria temporal del flask
        return redirect(url_for('map')) #manda al usuario a la siguiente pagina, en este caso dashboard
    else:
        return "Usuario o contraseña incorrectos", 401 #401 es el código de estado HTTP para "No autorizado".

@app.route('/map')
def dashboard(): #Define una nueva ruta en "/dashboard", que será la página a la que se accede tras un login exitoso.
    if 'usuario' in session:
        return render_template('map.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) #Inicia el servidor de Flask para ejecutar la aplicación.
