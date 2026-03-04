# Importamos la librería requests.
# Esta librería sirve para que nuestro programa pueda hacer peticiones HTTP
# a otros servicios (por ejemplo a Consul).
import requests


# Importamos Flask para crear el servidor web.
# render_template permite mostrar páginas HTML.
from flask import Flask, render_template


# Importamos el controlador de productos.
# Aquí es donde están las rutas que manejan los productos
# (crear producto, ver productos, actualizar stock, etc).
from products.controllers.product_controller import product_controller


# Importamos la conexión a la base de datos.
# db es el objeto que conecta Flask con MySQL usando SQLAlchemy.
from db.db import db


# Importamos CORS.
# CORS permite que otros servidores (como el frontend)
# puedan hacer peticiones a este microservicio.
from flask_cors import CORS


# Esta línea está comentada.
# flask_consulate sirve para registrar servicios automáticamente en Consul.
# from flask_consulate import Consul



# Aquí creamos la aplicación Flask.
# Esta aplicación será el servidor de nuestro microservicio.
app = Flask(__name__)


# Activamos CORS en la aplicación.
# Esto permite que el frontend se pueda comunicar con este servicio.
CORS(app)


# Cargamos las configuraciones definidas en config.py.
# Ahí está la conexión a la base de datos.
app.config.from_object('config.Config')


# Inicializamos la base de datos con Flask.
# Esto conecta la aplicación con MySQL.
db.init_app(app)



# -----------------------------
# RUTA DE HEALTH CHECK
# -----------------------------

# Esta ruta sirve para verificar si el microservicio está funcionando.
@app.route("/health", methods=["GET"])
def health():

    # Cuando alguien visita /health el servidor responde con:
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

        # Nombre del servicio.
        "Name": "micro_products",

        # Identificador único del servicio.
        "ID": "micro_products-1",

        # Dirección del servicio dentro de Docker.
        # Este nombre debe coincidir con el servicio en docker-compose.
        "Address": "micro_products",

        # Puerto donde corre el microservicio.
        "Port": 5003,

        # Configuración del health check.
        "Check": {

            # URL que Consul usará para verificar si el servicio está activo.
            "HTTP": "http://micro_products:5003/health",

            # Cada cuánto tiempo se hace la verificación.
            "Interval": "10s",

            # Tiempo máximo de espera de respuesta.
            "Timeout": "5s"
        }
    }



    # Intentamos registrar el servicio en Consul.
    try:

        # Enviamos una petición PUT al servidor de Consul.
        requests.put(
            "http://consul:8500/v1/agent/service/register",
            json=payload,
            timeout=5
        )

        # Si todo funciona mostramos este mensaje en la consola.
        print("[CONSUL] micro_products registered")

    except Exception as e:

        # Si ocurre un error lo mostramos en la consola.
        print("[CONSUL] registration failed:", e)



# Aquí ejecutamos la función para registrar el servicio
# cuando el microservicio arranca.
register_with_consul()



# -----------------------------
# REGISTRAR CONTROLADOR
# -----------------------------

# Aquí registramos el controlador de productos.
# Esto agrega todas las rutas definidas en product_controller
# a la aplicación Flask.
app.register_blueprint(product_controller)



# -----------------------------
# INICIO DEL SERVIDOR
# -----------------------------

# Esta condición verifica si este archivo se está ejecutando directamente.
if __name__ == '__main__':

    # Si es así, se inicia el servidor Flask.
    # El servidor empezará a escuchar peticiones HTTP.
    app.run()