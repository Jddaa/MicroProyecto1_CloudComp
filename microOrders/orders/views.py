# Importamos la librería requests.
# Esta librería permite que nuestro programa haga peticiones HTTP
# a otros servicios (por ejemplo a Consul).
import requests


# Importamos Flask para crear el servidor web
# y render_template para mostrar páginas HTML.
from flask import Flask, render_template


# Importamos el controlador de órdenes.
# Aquí es donde están las rutas que manejan las órdenes (crear orden,
# ver órdenes, etc.).
from orders.controllers.order_controller import order_controller


# Importamos la conexión a la base de datos.
# Este objeto db será usado para conectar Flask con MySQL usando SQLAlchemy.
from db.db import db


# Importamos CORS.
# CORS permite que otros servidores puedan hacer peticiones
# a este servicio.
from flask_cors import CORS


# Esta línea está comentada.
# flask_consulate sirve para registrar servicios automáticamente en Consul.
# from flask_consulate import Consul



# Aquí creamos la aplicación Flask.
# Esta será el servidor que correrá nuestro microservicio.
app = Flask(__name__)



# Aquí configuramos CORS.
# Esto permite que el frontend (que corre en otro puerto)
# pueda comunicarse con este microservicio.
CORS(
    app,

    # Permite enviar cookies o credenciales en las peticiones.
    supports_credentials=True,

    # Aquí se define qué origen puede acceder a este API.
    # En este caso el frontend corre en:
    # http://192.168.100.3:5001
    resources={r"/api/*": {"origins": ["http://192.168.100.3:5001"]}}
)



# Aquí cargamos las configuraciones definidas en el archivo config.py.
# Esto incluye:
# - conexión a la base de datos
# - secret key
app.config.from_object('config.Config')


# Inicializamos la base de datos con Flask.
# Esto conecta la aplicación con MySQL usando SQLAlchemy.
db.init_app(app)



# -----------------------------
# RUTA DE HEALTH CHECK
# -----------------------------

# Esta ruta sirve para comprobar si el microservicio está funcionando.
@app.route("/health", methods=["GET"])
def health():

    # Si alguien visita /health el servidor responde con:
    # {"status": "ok"}
    return {"status": "ok"}, 200



# -----------------------------
# REGISTRO DEL SERVICIO EN CONSUL
# -----------------------------

# Esta función registra el microservicio en Consul.
# Consul es una herramienta que permite que los servicios
# se descubran entre sí dentro de una arquitectura de microservicios.
def register_with_consul():

    # Este diccionario contiene la información del servicio
    # que vamos a registrar en Consul.
    payload = {

        # Nombre del servicio
        "Name": "micro_orders",

        # Identificador único del servicio
        "ID": "micro_orders-1",

        # Dirección del contenedor dentro de Docker
        "Address": "micro_orders",

        # Puerto donde corre este microservicio
        "Port": 5004,

        # Configuración del health check
        "Check": {

            # URL que Consul usará para verificar
            # si el servicio está vivo
            "HTTP": "http://micro_orders:5004/health",

            # Cada cuánto tiempo se hace la verificación
            "Interval": "10s",

            # Tiempo máximo de espera de respuesta
            "Timeout": "5s"
        }
    }


    # Intentamos registrar el servicio en Consul
    try:

        # Enviamos una petición PUT al servidor de Consul
        requests.put(
            "http://consul:8500/v1/agent/service/register",
            json=payload,
            timeout=5
        )

        # Si todo funciona, mostramos este mensaje en la consola
        print("[CONSUL] micro_orders registered")

    except Exception as e:

        # Si ocurre un error, lo mostramos en la consola
        print("[CONSUL] registration failed:", e)



# Aquí ejecutamos la función que registra el servicio
# justo cuando el microservicio arranca.
register_with_consul()



# -----------------------------
# REGISTRO DEL CONTROLADOR
# -----------------------------

# Aquí registramos el blueprint del controlador de órdenes.
# Esto hace que todas las rutas definidas en order_controller
# se agreguen a la aplicación.
app.register_blueprint(order_controller)



# -----------------------------
# INICIO DEL SERVIDOR
# -----------------------------

# Esta condición verifica si el archivo se está ejecutando directamente.
if __name__ == '__main__':

    # Si es así, se inicia el servidor Flask.
    # El servidor escuchará peticiones HTTP.
    app.run()