# Importa la librería requests, que permite hacer peticiones HTTP
# desde Python hacia otros servicios o APIs.
import requests

# Importa Flask para crear el servidor web,
# y render_template para cargar páginas HTML.
from flask import Flask, render_template

# Permite que otros dominios puedan hacer peticiones a este servidor
# (CORS = Cross-Origin Resource Sharing).
from flask_cors import CORS

# Esta línea está comentada. flask_consulate se usa para registrar
# servicios automáticamente en Consul.
# from flask_consulate import Consul


# Crea la aplicación Flask.
app = Flask(__name__)

# Habilita CORS para permitir comunicación con otros servicios.
CORS(app)

# Carga la configuración desde el archivo config.Config.
app.config.from_object('config.Config')


# -------------------------------
# RUTA DE HEALTH CHECK
# -------------------------------

# Esta ruta sirve para verificar si el servicio está funcionando.
@app.route("/health", methods=["GET"])
def health():

    # Devuelve un JSON indicando que el servicio está activo.
    return {"status": "ok"}, 200


# -------------------------------
# REGISTRO EN CONSUL
# -------------------------------

# Esta función registra el frontend en Consul,
# que es un sistema de descubrimiento de servicios.
def register_with_consul():

    # Datos que se enviarán a Consul para registrar el servicio.
    payload = {

        # Nombre del servicio
        "Name": "frontend",

        # ID único del servicio
        "ID": "frontend-1",

        # Dirección del servicio dentro de Docker o la red
        "Address": "frontend",

        # Puerto donde corre el frontend
        "Port": 5001,

        # Configuración del health check
        "Check": {

            # URL que Consul usará para verificar si el servicio está vivo
            "HTTP": "http://frontend:5001/health",

            # Cada cuánto tiempo se hace el chequeo
            "Interval": "10s",

            # Tiempo máximo de espera
            "Timeout": "5s"
        }
    }

    try:

        # Envía una petición PUT a Consul para registrar el servicio.
        requests.put(
            "http://consul:8500/v1/agent/service/register",
            json=payload,
            timeout=5
        )

        # Mensaje en consola indicando que se registró correctamente.
        print("[CONSUL] frontend registered")

    except Exception as e:

        # Si falla el registro, muestra el error.
        print("[CONSUL] registration failed:", e)


# Ejecuta la función para registrar el frontend en Consul.
register_with_consul()


# -------------------------------
# RUTAS QUE RENDERIZAN HTML
# -------------------------------

# Ruta principal del sitio.
@app.route('/')
def index():

    # Renderiza el archivo index.html.
    return render_template('index.html')


# Ruta que muestra la página de usuarios.
@app.route('/users')
def users():

    # Renderiza users.html
    return render_template('users.html')


# Ruta para editar un usuario específico.
@app.route('/editUser/<string:id>')
def edit_user(id):

    # Imprime el id recibido en la consola.
    print("id recibido",id)

    # Renderiza editUser.html y envía el id al template.
    return render_template('editUser.html', id=id)


# Ruta que muestra la página de productos.
@app.route('/products')
def products():

    # Renderiza products.html
    return render_template('products.html')


# Ruta para editar un producto específico.
@app.route('/editProduct/<string:id>')
def edit_products(id):

    # Imprime el id del producto en consola.
    print("id recibido", id)

    # Renderiza editProduct.html pasando el id.
    return render_template('editProduct.html', id=id)


# Ruta para mostrar la tienda (catálogo de productos).
@app.get("/shop")
def shop():

    # Renderiza shop.html
    return render_template("shop.html")


# Ruta para mostrar el carrito de compras.
@app.get("/cart")
def cart():

    # Renderiza cart.html
    return render_template("cart.html")


# Ruta del panel de administrador para ver órdenes.
@app.get("/admin/orders")
def admin_orders():

    # Renderiza ordersAdmin.html
    return render_template("ordersAdmin.html")


# Ruta donde el usuario puede ver sus propias órdenes.
@app.get("/my-orders")
def my_orders():

    # Renderiza ordersMy.html
    return render_template("ordersMy.html")


# -------------------------------
# INICIO DEL SERVIDOR
# -------------------------------

# Esta condición verifica si el archivo se está ejecutando directamente.
if __name__ == '__main__':

    # Inicia el servidor Flask.
    app.run()