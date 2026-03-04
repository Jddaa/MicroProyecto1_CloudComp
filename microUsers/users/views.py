# Importamos la librería requests.
# Esta librería permite que nuestro programa haga peticiones HTTP
# a otros servicios (por ejemplo a Consul).
import requests


# Importamos Flask para crear el servidor web.
# render_template se usa normalmente para mostrar páginas HTML.
from flask import Flask, render_template


# Importamos el controlador de usuarios.
# En este archivo están definidas las rutas que manejan los usuarios
# (crear usuario, login, ver usuarios, etc).
from users.controllers.user_controller import user_controller


# Importamos la conexión a la base de datos.
# db es el objeto que conecta Flask con MySQL usando SQLAlchemy.
from db.db import db


# Importamos CORS.
# CORS permite que otros servidores (como el frontend)
# puedan hacer peticiones a este microservicio.
from flask_cors import CORS


# Esta línea está comentada.
# flask_consulate es otra forma de registrar servicios en Consul.
# from flask_consulate import Consul



# Aquí creamos la aplicación Flask.
# Esta aplicación será el servidor de nuestro microservicio.
app = Flask(__name__)



# Activamos CORS con configuración específica.
# Esto permite que el frontend se comunique con este servicio.
CORS(

    app,

    # Permite enviar credenciales (por ejemplo cookies de sesión).
    supports_credentials=True,

    # Aquí se define qué servidor puede hacer peticiones.
    # En este caso el frontend corre en:
    # http://192.168.100.3:5001
    resources={r"/api/*": {"origins": ["http://192.168.100.3:5001"]}}
)



# Cargamos las configuraciones del archivo config.py.
# Allí está la conexión a la base de datos y otras configuraciones.
app.config.from_object('config.Config')



# Inicializamos la base de datos con Flask.
# Esto conecta el microservicio con MySQL.
db.init_app(app)



# -----------------------------
# RUTA DE HEALTH CHECK
# -----------------------------

# Esta ruta sirve para verificar si el microservicio está funcionando.
# Consul usa esta ruta para comprobar si el servicio está vivo.
@app.route("/health", methods=["GET"])
def health():

    # Si alguien visita /health el servidor responde:
    # {"status": "ok"}
    return {"status": "ok"}, 200



# -----------------------------
# REGISTRO DEL SERVICIO EN CONSUL
# -----------------------------

# Esta función registra este microservicio en Consul.
# Consul es una herramienta que permite que los microservicios
# se encuentren entre sí automáticamente.
def register_with_consul():

    # payload es un diccionario con la información del servicio.
    payload = {

        # Nombre del microservicio.
        "Name": "micro_users",

        # Identificador único del servicio.
        "ID": "micro_users-1",

        # Dirección del servicio dentro de Docker.
        "Address": "micro_users",

        # Puerto donde corre el microservicio.
        "Port": 5002,

        # Configuración del health check.
        "Check": {

            # URL que Consul usará para verificar si el servicio está activo.
            "HTTP": "http://micro_users:5002/health",

            # Cada cuánto tiempo se revisa el servicio.
            "Interval": "10s",

            # Tiempo máximo de espera de respuesta.
            "Timeout": "5s"
        }
    }


    # Intentamos registrar el servicio en Consul.
    try:

        # Enviamos una petición PUT al servidor de Consul
        # para registrar este microservicio.
        requests.put(
            "http://consul:8500/v1/agent/service/register",
            json=payload,
            timeout=5
        )

        # Si funciona mostramos este mensaje en la consola.
        print("[CONSUL] micro_users registered")

    except Exception as e:

        # Si ocurre un error lo mostramos en la consola.
        print("[CONSUL] registration failed:", e)



# Aquí ejecutamos la función para registrar el servicio
# cuando el microservicio arranca.
register_with_consul()



# -----------------------------
# REGISTRAR CONTROLADOR
# -----------------------------

# Aquí registramos el controlador de usuarios.
# Esto agrega todas las rutas definidas en user_controller
# a la aplicación Flask.
app.register_blueprint(user_controller)



# -----------------------------
# INICIO DEL SERVIDOR
# -----------------------------

# Esta condición verifica si este archivo se está ejecutando directamente.
if __name__ == '__main__':

    # Si es así, se inicia el servidor Flask.
    # El servidor empezará a escuchar peticiones HTTP.
    app.run()