from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Bienveides a ChamiTinder</p> <p>¿Alguna vez te has cruzado con alguien en cafeta, en el comedor o en una fiesta de abajo y has pensado: ‘Me encantaría hablar con esa persona’? ChamiTinder convierte esas dudas y miedos en oportunidades reales. Conecta, haz match y conoce a quienes comparten pasillos, risas y noches de estudio contigo. Porque en el colegio mayor, el amor (o la amistad) está a solo un click de distancia.</p> <p>Pulsa aquí para encontrar el amor<p/p> <a href='/register'>Regístrate</a>"

@app.route("/register")
def register():
    return "<p>Rellena con tus datos</p> <form action='/submit_registration' method='post'> Nombre y apellidos <input type='text' name='username' placeholder=' '><br> Número de habitación <input type='number' name='room' placeholder=' '><br> Email <input type='email' name='email' placeholder=' '> <br> <button type='submit'>Registrarse</button> </form>"

# crear la base de datos
@app.route("/setup")
def setup():
    # crear la base de datos y la tabla de usuarios
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    try:
        conexion.execute('''CREATE TABLE IF NOT EXISTS usuarios
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    room INTEGER NOT NULL,
                    email TEXT NOT NULL
                         );''')
    except sqlite3.OperationalError:
        print("La tabla ya existe.")
    conexion.close()
    return "<p>Base de datos creada con éxito.</p>"

@app.route("/stats")
def stats():
    import sqlite3
    # conectar a la base de datos y contar los usuarios
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]
    # listar todos los usuarios y ponerlos en una lista
    cursor.execute("SELECT username FROM usuarios")
    usuarios = cursor.fetchall()
    usuarios_list = [usuario[0] for usuario in usuarios]
    # dejar la lista en una tabla html
    usuarios_html = "<ul>" + "".join(f"<li>{usuario}</li>" for usuario in usuarios_list) + "</ul>"
    # mostrar el número de usuarios y la lista de usuarios
    # cerrar la conexión
    conexion.close()
    return f"<p>Hay {count} usuarios registrados en ChamiTinder.</p> <p>Usuarios:</p> {usuarios_html}"

# Parte 1: registro de los ususarios
@app.route("/submit_registration", methods=["POST"])
def submit_registration():
    # guardar en variables los datos del formulario de un usuario
    username = request.form.get("username")
    room = request.form.get("room") 
    email = request.form.get("email")
    # ahora guardo los datos en base de datos
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    conexion.execute("INSERT INTO usuarios (username, room, email) VALUES (?, ?, ?)", (username, room, email))
    conexion.commit()
    conexion.close()
    # Aquí se procesaría el registro del usuario
    return "<p>Registro exitoso. En unos días podrás introducir tu/s crush/es! <3 </p>"


#Parte 2: Inicio sesion de usuarios e introducción de crushes de cada usuario
#@app.route("/login")
#def login():
    #return "<p>Inicia sesión</p> <form action='/submit_login' method='post'> <input type='text' name='username' placeholder='Nombre y apellidos'> <button type='submit'>Iniciar sesión</button> </form>"
#@app.route("/submit_login", methods=["POST"])
#def submit_login():
#    username = request.form.get("username")
#    room = request.form.get("room")
#    email = request.form.get("email")
#   return f"<a href='/log'>Iniciar Sesión</a>
#@app.route("/log")
#def log():
#    return """
#       <p>En la siguiente lista verás todos los registrados en Chami Tinder. Podrás escoger entre ellos todas las personas con las que quieras hacer match </p> <form action='/submit_crushes' method='post'> <input type='text' name='crushes' placeholder='Crushes (separados por comas)'> <button type='submit'>Enviar</button> </form>"
#       <form action
