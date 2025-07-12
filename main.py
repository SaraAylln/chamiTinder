from flask import Flask, redirect, session
from flask import request
import sqlite3
from flask_session import Session 

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"  # O redis, etc.
app.config["SESSION_PERMANENT"] = False  # Sesión no permanente (expira al cerrar el navegador)
Session(app)

@app.route("/")
def hello_world():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            h1, .bienvenida {
                text-align: center;
            }
            .bienvenida {
                padding: 20px;
                border-radius: 10px;
                background: #fff;
            }
        </style>
    </head>
    <body>
        <h1>Bienvenides a ChamiTinder</h1>
        <div class="bienvenida">
            <img src='https://i.pinimg.com/originals/80/fb/6f/80fb6fcab27a2c8d6a2141c840f5e1cc.gif' width='400'><br>
            <p>¿Alguna vez te has cruzado con alguien en cafeta, en el comedor o en una fiesta de abajo y has pensado: ‘Me encantaría hablar con esa persona’? ChamiTinder convierte esas dudas y miedos en oportunidades reales. Conecta, haz match y conoce a quienes comparten pasillos, risas y noches de estudio contigo. Porque en el colegio mayor, el amor (o la amistad) está a solo un click de distancia.</p>
            <a href='/register'>Regístrate</a> <p> O si ya estás registrado, <a href='/login'>Inicia sesión</a></p>
    </body>
    </html>
    """

@app.route("/register")
def register():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            h1 {
                text-align: center;
            }
            .bienvenida {
                padding: 20px;
                border-radius: 10px;
                background: #fff;
                text-align: left;
                min-width: 350px;
            }
            form {
                margin-top: 20px;
            }
            input, button, select {
                margin: 8px 0;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #d81b60;
                width: 95%;
                box-sizing: border-box;
            }
            button {
                background-color: #d81b60;
                color: #fff;
                border: 1px solid #d81b60;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Registro en ChamiTinder</h1>
        <div class="bienvenida">
            <p>Rellena con tus datos</p>
            <form action='/submit_registration' method='post'>
                Nombre por el que te conocen <input type='text' name='username' placeholder=' ' required><br>
                Número de habitación <input type='number' name='room' placeholder=' ' required><br>
                Email <input type='email' name='email' placeholder=' ' required><br>
                Crea una contraseña <input type='password' name='password' placeholder=' ' required><br>
                <button type='submit'>Registrarse</button>
            </form>
        </div>
    </body>
    </html>
    """

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
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                         );''')
        conexion.execute("CREATE TABLE IF NOT EXISTS crushes (username TEXT NOT NULL, crush TEXT NOT NULL)")
    except sqlite3.OperationalError:
        print("La tabla ya existe.")

    conexion.close()
    return "<p>Base de datos creada con éxito.</p>"


@app.route("/stats")
def stats():
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]
    cursor.execute("SELECT username, room, email FROM usuarios ORDER BY username ASC")
    usuarios = cursor.fetchall()
    conexion.close()

    # Construir la tabla HTML
    tabla_html = """
    <table style='width:100%; border-collapse:collapse;'>
        <tr>
            <th style='border:1px solid #d81b60; padding:8px;'>Nombre</th>
            <th style='border:1px solid #d81b60; padding:8px;'>Habitación</th>
            <th style='border:1px solid #d81b60; padding:8px;'>Email</th>
        </tr>
    """
    for username, room, email in usuarios:
        tabla_html += f"""
        <tr>
            <td style='border:1px solid #d81b60; padding:8px;'>{username}</td>
            <td style='border:1px solid #d81b60; padding:8px;'>{room}</td>
            <td style='border:1px solid #d81b60; padding:8px;'>{email}</td>
        </tr>
        """
    tabla_html += "</table>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            h1, .bienvenida {{
                text-align: center;
            }}
            .bienvenida {{
                padding: 20px;
                border-radius: 10px;
                background: #fff;
            }}
            table {{
                margin-top: 20px;
                background: #fff;
            }}
            th {{
                background: #f8bbd0;
            }}
        </style>
    </head>
    <body>
        <h1>Estadísticas de ChamiTinder</h1>
        <div class="bienvenida">
            <p>Hay {count} usuarios registrados en ChamiTinder.</p>
            <p>Usuarios:</p>
            {tabla_html}
        </div>
    </body>
    </html>
    """

# Parte 1: registro de los ususarios
@app.route("/submit_registration", methods=["POST"])
def submit_registration():
    username = request.form.get("username")
    room = request.form.get("room") 
    email = request.form.get("email")
    password = request.form.get("password")
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    conexion.execute("INSERT INTO usuarios (username, room, email, password) VALUES (?, ?, ?, ?)", (username, room, email, password))
    conexion.commit()
    conexion.close()
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            h1, .bienvenida {
                text-align: center;
            }
            .bienvenida {
                padding: 20px;
                border-radius: 10px;
                background: #fff;
            }
        </style>
    </head>
    <body>
        <h1>¡Registro exitoso!</h1>
        <div class="bienvenida">
            <p>En unos días podrás introducir tu/s crush/es! &lt;3</p>
            <a href='/'>Volver al inicio</a>
        </div>
    </body>
    </html>
    """


#Parte 2: Inicio sesion de usuarios e introducción de crushes de cada usuario
# primero construyo una pagina para que los usuarios inicien sesión con sus datos y posteriormente puedan introducir sus crushes
@app.route("/login")
def login():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            h1, .bienvenida {
                text-align: center;
            }
            .bienvenida {
                padding: 20px;
                border-radius: 10px;
                background: #fff;
                text-align: left;
                min-width: 350px;
            }
            form {
                margin-top: 20px;
            }
            input, button, select {
                margin: 8px 0;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #d81b60;
                width: 95%;
                box-sizing: border-box;
            }
            button {
                background-color: #d81b60;
                color: #fff;
                border: 1px solid #d81b60;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Iniciar Sesión</h1>
        <div class="bienvenida">
            <form action='/submit_login' method='post'>
                Tu email <input type='email' name='email' placeholder=' ' required><br>
                Contraseña <input type='password' name='contraseña' placeholder=' ' required><br>
                <button type='submit'>Iniciar sesión</button>
            </form>
        </div>
    </body>
    </html>
    """
@app.route("/submit_login", methods=["POST"])
def submit_login():
    email = request.form.get("email")
    contraseña = request.form.get("contraseña")
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT username FROM usuarios WHERE email=? AND password=?", (email, contraseña))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario:
        # iniciamos la sesion 
        username = usuario[0]
        # guardamos el nombre de usuario en la sesión (esto es un ejemplo, necesitarías configurar sesiones en Flask)
        session['username'] = username 
        return redirect("/introducir_crushes")
    else:  
        return """
        <html>
        <head>
            <style>
                body {
                    background-color: #fce4ec;
                    color: #333;
                    font-family: Verdana, Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                }
                h1, .bienvenida {
                    text-align: center;
                }
                .bienvenida {
                    padding: 20px;
                    border-radius: 10px;
                    background: #fff;
                }
            </style>
        </head>
        <body>
            <h1>Error de inicio de sesión</h1>
            <a href='/login'>Volver a intentar</a>
        </body>
        </html>
        """
  
# introducir los crushes de cada usuario
@app.route("/introducir_crushes", methods=["GET", "POST"])
def introducir_crushes():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT username, room FROM usuarios ORDER BY username ASC")
    usuarios = cursor.fetchall()
    conexion.close()

    # Construir la tabla con checkboxes
    crushes = "<form action='/guardar_crushes' method='post'><table style='width:100%; border-collapse:collapse;'>"
    crushes += "<tr><th style='border:1px solid #d81b60; padding:8px;'>Selecciona tus crushes</th></tr>"
    for username, room in usuarios:
        crushes += f"<tr><td style='border:1px solid #d81b60; padding:8px;'><input type='checkbox' name='crushes' value='{username}'> {username} (Hab. {room})</td></tr>"
    crushes += "</table><button type='submit'>Guardar crushes</button></form>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            h1, .bienvenida {{
                text-align: center;
            }}
            .bienvenida {{
                padding: 20px;
                border-radius: 10px;
                background: #fff;
            }}
            table {{
                margin-top: 20px;
                background: #fff;
            }}
            th {{
                background: #f8bbd0;
            }}
            button {{
                background-color: #d81b60;
                color: #fff;
                border: 1px solid #d81b60;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>Introduce tus crushes</h1>
        <div class="bienvenida">
            {crushes}
        </div>
    </body>
    </html>
    """


#crear otra tabla de base de datos para guardar los crushes marcados en la tabla_html
@app.route("/guardar_crushes", methods=["POST"])
def guardar_crushes():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    seleccionados = request.form.getlist("crushes")
    # Guardar los crushes seleccionados en la base de datos
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    for crush in seleccionados:
        cursor.execute("INSERT INTO crushes (username, crush) VALUES (?, ?)", (username, crush))
    seleccionados_html = ", ".join(seleccionados) if seleccionados else "No seleccionaste ningún crush."
    conexion.close()

    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #fce4ec;
                color: #333;
                font-family: Verdana, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            h1, .bienvenida {{
                text-align: center;
            }}
            .bienvenida {{
                padding: 20px;
                border-radius: 10px;
                background: #fff;
            }}
            button {{
                background-color: #d81b60;
                color: #fff;
                border: 1px solid #d81b60;
                cursor: pointer;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>¡Crushes guardados!</h1>
        <div class="bienvenida">
            <p>Tus crushes seleccionados:</p>
            <p>{seleccionados_html}</p>
            <a href='/'><button>Volver al inicio</button></a>
        </div>
    </body>
    </html>
    """

