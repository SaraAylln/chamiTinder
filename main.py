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
                background-color: #fcbbd1;
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
    # verificar fase de la aplicación almacenada en la tabla de base de datos
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT valor_variable FROM variables WHERE nombre_variable='fase'")
    fase = cursor.fetchone()
    conexion.close()
    if fase and fase[0] == '2':
        return redirect("/pagina_espera2")

    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fcbbd1;
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
            <p><b>Rellena con tus datos</b></p>
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
        conexion.execute('''CREATE TABLE crushes  
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         username TEXT NOT NULL, 
                         crush TEXT NOT NULL, 
                         FOREIGN KEY (username) REFERENCES usuarios(username), 
                         FOREIGN KEY (crush) REFERENCES usuarios(username), 
                         UNIQUE (username, crush)
                         );''')

        conexion.commit()
        conexion.execute('''
            CREATE TABLE IF NOT EXISTS variables (
                nombre_variable TEXT PRIMARY KEY,
                valor_variable TEXT
                    );''') 
                 
        conexion.execute("INSERT OR IGNORE INTO variables (nombre_variable, valor_variable) VALUES (?, ?)", ('fase', '1'))
        conexion.commit()
        
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
                background-color: #fcbbd1;
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
                background-color: #fcbbd1;
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
    # verificar fase de la aplicación almacenada en la tabla de base de datos
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT valor_variable FROM variables WHERE nombre_variable='fase'")
    fase = cursor.fetchone()
    conexion.close()
    if 'username' in session:
        return redirect("/inicio")

    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fcbbd1;
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
                <a href='/register'>¿No tienes cuenta? Regístrate aquí</a><br>
                <a href='/lostPass'>¿Has olvidado tu contraseña?</a>
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
    cursor.execute("SELECT username, room FROM usuarios WHERE email=? AND password=?", (email, contraseña))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario:
        # iniciamos la sesion 
        username = usuario[0]
        room = usuario[1]
        # guardamos el nombre de usuario en la sesión (esto es un ejemplo, necesitarías configurar sesiones en Flask)
        session['username'] = username 
        session['email'] = email
        session['habitacion'] = room

        return redirect("/inicio")
    else:  
        return """
        <html>
        <head>
            <style>
                body {
                    background-color: #fcbbd1;
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
            <p>Si no tienes cuenta, <a href='/register'>regístrate aquí</a></p>
            <p>Si has olvidado tu contraseña, pulsa <a href='/lostPass'> aquí</a> .</p>
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
                background-color: #fcbbd1;
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

# NOOOO FUNCIONA MANDAR LOS CORREOS. MANDA  "No new matches found after saving crushes" Y SÍ HAY MATCH.

def send_match_email(user1_email, user2_email, user1_name, user2_name):
    import smtplib
    from email.mime.text import MIMEText

    print(f"DEBUG: Enviando email de match a {user1_email} y {user2_email}")
    print(f"Asunto: ¡Tienes un nuevo Match en ChamiTinder!")
    print(f"Cuerpo para {user1_name}: ¡Felicidades! Has hecho match con {user2_name}. ¡Contacta con tu crush!")
    print(f"Cuerpo para {user2_name}: ¡Felicidades! Has hecho match con {user1_name}. ¡Contacta con tu crush!")
    
    
    sender_email = "cupidechamitinder@gmail.com"
    sender_password = "amge hsbo rvej scol"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    try:
        msg1 = MIMEText(f"¡Felicidades, {user1_name}! Has hecho match con {user2_name}. ¡Es hora de contactar con tu crush!")
        msg1["Subject"] = "¡Tienes un nuevo Match en ChamiTinder!"
        msg1["From"] = sender_email
        msg1["To"] = user1_email

        msg2 = MIMEText(f"¡Felicidades, {user2_name}! Has hecho match con {user1_name}. ¡Es hora de contactar con tu crush!")
        msg2["Subject"] = "¡Tienes un nuevo Match en ChamiTinder!"
        msg2["From"] = sender_email
        msg2["To"] = user2_email

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg1)
            server.send_message(msg2)
        print(f"Emails de match enviados con éxito a {user1_email} y {user2_email}")
    except Exception as e:
         print(f"ERROR: No se pudo enviar el email de match: {e}")


@app.route("/guardar_crushes", methods=["POST"])
def guardar_crushes():
    if 'username' not in session:
        return redirect("/login")

    username = session['username']
    seleccionados = request.form.getlist("crushes")

    conexion = None
    try:
        conexion = sqlite3.connect("usuariosChamiTinder.db")
        cursor = conexion.cursor()

        # 1. Get current matches *before* updating crushes (for new match detection)
        cursor.execute("""
            SELECT c1.username, c1.crush
            FROM crushes AS c1
            JOIN crushes AS c2 ON c1.username = c2.crush AND c1.crush = c2.username
            WHERE c1.username != c1.crush
        """)
        existing_matches_raw = cursor.fetchall()
        existing_matches = {tuple(sorted(match)) for match in existing_matches_raw}

        # Introducir los seleccionados como crushes en tabla crushes
        for crush in seleccionados:
            if crush != username: # Prevent self-crushes
                try:
                    cursor.execute("INSERT INTO crushes (username, crush) VALUES (?, ?)", (username, crush))
                except sqlite3.IntegrityError:
                    # This means the (username, crush) pair already exists
                    print(f"INFO: Crush '{crush}' for user '{username}' already exists. Skipping insertion.")
                    pass # Simply skip this entry if it's a duplicate

        conexion.commit() 

        # 3. Find all matches *after* updating crushes
        cursor.execute("""
            SELECT c1.username, c1.crush
            FROM crushes AS c1
            JOIN crushes AS c2 ON c1.username = c2.crush AND c1.crush = c2.username
            WHERE c1.username != c1.crush
        """)
        current_matches_raw = cursor.fetchall()
        current_matches = {tuple(sorted(match)) for match in current_matches_raw}

        # 4. Identify NEW matches
        new_matches = current_matches - existing_matches

        # 5. Get emails for users involved in new matches and send emails
        if new_matches:
            all_involved_users = set()
            for u1, u2 in new_matches:
                all_involved_users.add(u1)
                all_involved_users.add(u2)

            placeholders = ','.join('?' for _ in all_involved_users)
            cursor.execute(f"SELECT username, email FROM usuarios WHERE username IN ({placeholders})", tuple(all_involved_users))
            user_emails = {row[0]: row[1] for row in cursor.fetchall()}

            for u1, u2 in new_matches:
                email1 = user_emails.get(u1)
                email2 = user_emails.get(u2)
                if email1 and email2:
                    send_match_email(email1, email2, u1, u2)
                    print (f""" email enviado""")
                else:
                    print(f"WARNING: No se pudo encontrar email para {u1} o {u2} para enviar match.")
        else:
            print("No new matches found after saving crushes.")

        seleccionados_html = ", ".join(seleccionados) if seleccionados else "No seleccionaste ningún crush."
        # enviar correo electrónico a los usuarios con sus crushes guardados


        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Crushes Guardados</title>
            <style>
                body {{
                    background-color: #fce4ec;
                    color: #4a4a4a;
                    font-family: 'Verdana', sans-serif;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                    box-sizing: border-box;
                }}
                .container {{
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    max-width: 500px;
                    width: 100%;
                }}
                h1 {{
                    color: #d81b60;
                    margin-bottom: 20px;
                    font-size: 2.5em;
                }}
                p {{
                    font-size: 1.1em;
                    line-height: 1.6;
                    margin-bottom: 10px;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #d81b60;
                }}
                button {{
                    background-color: #d81b60;
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 25px;
                    margin-top: 25px;
                    font-size: 1.1em;
                    cursor: pointer;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }}
                button:hover {{
                    background-color: #c2185b;
                    transform: translateY(-2px);
                }}
                a {{
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Crushes guardados!</h1>
                <p>Tus crushes seleccionados:</p>
                <p class="highlight">{seleccionados_html}</p>
                <p> Si haces match con alguno de tus crushes, te llegará un email, estate alerta!</p>
                <a href='/inicio'><button>Volver al inicio</button></a>
            </div>
        </body>
        </html>
        """
    except sqlite3.Error as e:
        print(f"Error de base de datos al guardar crushes o buscar matches: {e}")
        if conexion:
            conexion.rollback()
        return f"Error al guardar tus crushes o buscar matches: {e}", 500
    finally:
        if conexion:
            conexion.close()
# ver la tabla de usuarios con sus crushes
@app.route("/stats2")
def stats2():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT username, crush FROM crushes ORDER BY username ASC")   
    crushes = cursor.fetchall()
    conexion.close()

    # Construir la tabla HTML
    tabla_html = """
    <table style='width:100%; border-collapse:collapse;'>
        <tr>
            <th style='border:1px solid #d81b60; padding:8px;'>Usuario</th>
            <th style='border:1px solid #d81b60; padding:8px;'>Crushes</th>
        </tr>
    """
    for username, crush in crushes:
        tabla_html += f"""
        <tr>
            <td style='border:1px solid #d81b60; padding:8px;'>{username}</td>
            <td style='border:1px solid #d81b60; padding:8px;'>{crush}</td>
        </tr>
        """
    tabla_html += "</table>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #fcbbd1;
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
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Mis Crushes</h1>
        <div class="bienvenida">
            <p>Aquí están tus crushes:</p>
            {tabla_html}
            <a href='/'><button>Volver al inicio</button></a>
        </div>
    </body>
    </html>
    """


@app.route("/admin")
def admin():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    if session['username'] != 'admin':
        return "No tienes permisos para acceder a esta página."
    username = session['username']
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT username, room FROM usuarios ORDER BY username ASC")
    usuarios = cursor.fetchall()
    conexion.close()

    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #ad1457;
                color: #fff;
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
                min-width: 350px;
                color: #333;
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
        <h1>Panel de Administración</h1>
        <div class="bienvenida">
            <p>Bienvenido, <b>{username}</b>.</p>
            <a href='/stats'><button>Usuarios registrados</button></a>
            <a href='/stats2'><button>Ver crushes de los usuarios</button></a>
            <a href='/estadoChamiTinder'><button>Estado ChamiTinder</button></a>
        </div>
    </body>
    </html>
    """

@app.route("/estadoChamiTinder")
def estadoChamiTinder():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    if session['username'] != 'admin':
        return "No tienes permisos para acceder a esta página."
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]
    conexion.close()
    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #ad1457;
                color: #fff;
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
                color: #333;
                min-width: 350px;
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
        <h1>Estado de ChamiTinder</h1>
        <div class="bienvenida">
            <a href='/ejecFase1'><button> Fase 1 </button></a>
            <p>Fase 1: registro todos los usuarios e inicio de sesión; seleccion crushes desactivada</p>
            <a href='/ejecFase2'><button> Fase 2 </button></a>
            <p>Fase 2: registro desactivado; inicio de sesión y seleccion de crushes activadas (si activas la fase 2 se va a mandar un correo a todos los registrados para que seleccionen crushes) </p>
        </div>
    </body>
    </html>
    """


# crear tabla de base de dato para guardar pagina a la que se dirige /login en funcion de la fase

redirect_login = ""
@app.route("/ejecFase1")
def ejecFase1():
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE variables SET valor_variable='1' WHERE nombre_variable='fase'")
    conexion.commit()
    return "ok"


@app.route("/pagina_espera")
def pagina_espera():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fcbbd1;
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
        <h1>Fase 1 en ejecución</h1>
        <div class="bienvenida">
            <p> Más adelante podrás introducir tus crushes!!!</p>
            <a href='/'>Volver a la página de inicio</a>

        </div>
    </body> 
    </html>
    """

@app.route("/ejecFase2")
def ejecFase2():
    # Verificar si el usuario ha iniciado sesión
    if 'username' not in session:
        return redirect("/login")
    if session['username'] != 'admin':
        return "No tienes permisos para acceder a esta página."
    
    # Fase 2: registro desactivado; inicio de sesión y seleccion de crushes activada
    # Actualizar la fase en la base de datos y enviar correos a los usuarios
    import sqlite3
    # registro desactivado; inicio de sesión y seleccion de crushes activada
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()

        # 1. Update the phase (already correct)
    cursor.execute("UPDATE variables SET valor_variable='2' WHERE nombre_variable='fase'")
    conexion.commit() # Commit the phase update

        # 2. Get all user emails for sending notifications
    cursor.execute("SELECT email FROM usuarios") # Select only the emails
    users_emails = cursor.fetchall() # Get all results


    if users_emails:    
        for user_email in users_emails:
            email = user_email[0]  # Extract the email from the tuple
            # 3. Send email to each user
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders
            from email.utils import formataddr

            sender_email = "cupidechamitinder@gmail.com"
            sender_name = "ChamiTinder"
            sender_password = "amge hsbo rvej scol"
            receiver_email = email
            subject = "Selección crushes - ChamiTinder"

            body = f"""
            <html>
            <body>
                <p>Hola,</p>
                <p>Desde hoy mismo puedes seleccionar tus crushes entre las personas que se han registrado en ChamiTinder! </p>
                <p>Si haces match te llegará un correo indicando con quien <333</p>
                <p>Mucha suerte bb</p>
                <p>Saludos,</p>
                <p>Cupide ChamiTinder</p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart()
            msg['From'] = formataddr((sender_name, sender_email))
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
    return "ok"
                

@app.route("/pagina_espera2")
def pagina_espera2():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fcbbd1;
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
        <h1>Ya no te puedes registrar!! Lo sentimos :(( </h1>
    <div>
    </body>
    </html>
    """


@app.route("/inicio")
def inicio():
    if 'username' not in session:
        return redirect("/login")
    username = session['username']  

    # recuperar fase 
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT valor_variable FROM variables WHERE nombre_variable='fase'")
    fase = cursor.fetchone()
    conexion.close()
    # en fase 1 pagina con fondo rosa igual que las demás con una imagen y mensaje de te avisaremos cuando pupedas introducir tus crushes
    if fase and fase[0] == '1':
        return """    <html>
        <head>
            <style>
                body {
                    background-color: #fcbbd1;
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
            <h1>Bienvenide a ChamiTinder</h1>
            <div class="bienvenida">
                <p>Hola, """+ username+ """</p>
                <p> Tu correo electrónico es: """ + session['email'] + """
                <p> Tu habitación es: """ + str(session['habitacion']) + """
                <p> Te avisaremos cuando puedas introducir tus crushes!</p>
                <img src='https://www.hermanitas.net/img/subidas/descripcion_1735670847.gif' width='400'><br>
                
        </body>
        </html>
        """
    else:
        # en fase 2 pagina con fondo rosa igual que las demás con una imagen y boton para introducir tus crushes
        return """
        <html>
        <head>
            <style>
                body {
                    background-color: #fcbbd1;
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
                button {
                    background-color:
                    #d81b60;
                    color: #fff;
                    border: 1px solid
                    #d81b60;
                    cursor: pointer;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Bienvenido/a a ChamiTinder</h1>
            <div class="bienvenida">
                <p>Hola, """+ username + """</p>
                <p> Ahora puedes introducir tus crushes!</p>
                <img src='https://i.pinimg.com/originals/80/fb/6f/80fb6fcab27a2c8d6a2141c840f5e1cc.gif' width='400'><br>
                <a href='/introducir_crushes'><button> Introducir mis crushes </button></a>
                <a href='/crushes_de_cada_usuario'><button> Ver mis crushes </button></a>
            </div>
        </body>
        </html>
        """     


# pagina para recuperar contraseña
@app.route("/lostPass")
def lostPass():
    return """
    <html>
    <head>
        <style>
            body {
                background-color: #fcbbd1;
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
        <h1>Recuperar contraseña</h1>
        <div class="bienvenida">
            <p> Escribe aqui tu email para recuperar tu contraseña</p>
            <form action='/submit_lostPass' method='post'>
                Email <input type='email' name='email' placeholder=' ' required><br>
                <button type='submit'>Recuperar contraseña</button>
            </form>
        </div>
    </body>
    </html>
    """

# enviar un email al usuario con su contraseña usando la api de google
@app.route("/submit_lostPass", methods=["POST"])
def submit_lostPass():
    email = request.form.get("email")
    conexion = sqlite3.connect("usuariosChamiTinder.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE email=?", (email,))
    password = cursor.fetchone()
    conexion.close()

    if password:
        # Enviamos al usuario un email con su contraseña via api de google
        password = password[0]
        # credenciales de la api de google
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        from email.utils import formataddr

        sender_email = "cupidechamitinder@gmail.com"
        sender_name = "ChamiTinder"
        sender_password = "amge hsbo rvej scol"
        receiver_email = email
        subject = "Recuperación de contraseña - ChamiTinder"

        body = f"""
        <html>
        <body>
            <p>Hola,</p>
            <p>Tu contraseña de ChamiTinder es: <b>"""+password+"""</b></p>
            <p>Saludos,</p>
            <p>Cupide ChamiTinder</p>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            return """
            <html>
            <head>
                <style>
                    body {
                        background-color: #fcbbd1;
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
                <h1>¡Contraseña enviada!</h1>
                <div class="bienvenida">
                    <p>Tu contraseña ha sido enviada a tu email.</p>
                    <a href='/login'>Volver a iniciar sesión</a>
                </div>
            </body>
            </html>
            """
        except Exception as e:
            return f"""
            <html>
            <head>
                <style>
                    body {{
                        background-color: #fcbbd1;
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
                </style>
            </head>
            <body>
                <h1>Error al enviar el email</h1>
                <div class="bienvenida">
                    <p>Hubo un error al enviar el email. Por favor, inténtalo de nuevo más tarde.</p>
                    <p>Error: """+str(e)+"""</p>
                    <a href='/lostPass'>Volver a intentar</a>
                </div>
            </body>
            </html>
            """

import sqlite3
from flask import Flask, session, redirect, render_template_string # Assuming Flask and session are used



#cada usuario solo puede ver sus crushes, no los de los demás
@app.route("/crushes_de_cada_usuario")
def crushes_de_cada_usuario():
    # Verify user session
    if 'username' not in session:
        return redirect("/login")

    # Get the username of the currently logged-in user
    logged_in_username = session['username']
    conexion = None # Initialize to None for the finally block
    user_crushes_data = [] # To store only the current user's crushes

    try:
        conexion = sqlite3.connect("usuariosChamiTinder.db")
        cursor = conexion.cursor()

        # Modified SQL query:
        # SELECT only the 'crush_username' for the 'logged_in_username'
        cursor.execute(
            "SELECT crush FROM crushes WHERE username = ? ORDER BY crush ASC",
            (logged_in_username,) # Pass the username as a parameter for security
        )
        user_crushes_data = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Database error fetching user's crushes: {e}")
        return f"Error al cargar tus crushes: {e}", 500
    finally:
        if conexion:
            conexion.close() # Ensure the connection is always closed

    
    crushes_list_for_display = [row[0] for row in user_crushes_data]
    crushes_str = ", ".join(crushes_list_for_display) if crushes_list_for_display else "Aún no has seleccionado ningún crush."

    tabla_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tus Crushes</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Inter', sans-serif; background-color: #fce4ec; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
            .container {{ background-color: white; padding: 2rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); max-width: 600px; width: 90%; }}
            h1 {{ color: #d81b60; text-align: center; margin-bottom: 1.5rem; }}
            .crushes-list {{
                background-color: #fce4ec; /* Light pink background */
                border: 1px solid #d81b60; /* Pink border */
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
                text-align: center;
                font-size: 1.1em;
                color: #4a4a4a;
            }}
            .button-link {{
                display: inline-block;
                background-color: #d81b60;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                text-decoration: none;
                margin-top: 20px;
                transition: background-color 0.3s ease;
            }}
            .button-link:hover {{
                background-color: #c2185b;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-3xl font-bold">¡Tus Crushes!</h1>
            <div class="crushes-list">
                <p><strong>{crushes_str}</strong></p>
            </div>
            <div style="text-align: center;">
                <a href="/inicio" class="button-link">Volver al inicio</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(tabla_html)

