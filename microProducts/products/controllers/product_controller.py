# Importamos herramientas de Flask.
# Blueprint se usa para organizar rutas en archivos separados.
# request sirve para leer información que envía el cliente (por ejemplo un formulario o JSON).
# jsonify convierte datos de Python a formato JSON, que es el formato que usan las APIs.
from flask import Blueprint, request, jsonify

# Importamos el modelo de productos.
# Este modelo representa la tabla de productos en la base de datos.
from products.models.product_model import Products

# Importamos la conexión a la base de datos.
# db permite guardar, actualizar y borrar información en MySQL usando SQLAlchemy.
from db.db import db


# Creamos un Blueprint llamado product_controller.
# Esto agrupa todas las rutas relacionadas con productos.
product_controller = Blueprint("product_controller", __name__)



# -----------------------------
# OBTENER TODOS LOS PRODUCTOS
# -----------------------------

# Esta ruta responde a peticiones GET en:
# /api/products
@product_controller.route('/api/products', methods=['GET'])
def get_products():

    # Este print solo muestra un mensaje en la consola del servidor.
    print("Listando de productos")

    # Aquí consultamos TODOS los productos que hay en la base de datos.
    products = Products.query.all()

    # Convertimos los productos a un formato JSON.
    # Esto es necesario para enviarlos como respuesta al cliente.
    result = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        }
        for product in products
    ]

    # Devolvemos la lista de productos en formato JSON.
    return jsonify(result)



# -----------------------------
# OBTENER UN PRODUCTO POR ID
# -----------------------------

# Esta ruta responde a peticiones GET en:
# /api/products/{id}
@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    # Mensaje que se muestra en la consola del servidor.
    print("Obteniendo Producto")

    # Buscamos el producto por su ID en la base de datos.
    # Si no existe, Flask devuelve automáticamente error 404.
    product = Products.query.get_or_404(product_id)

    # Devolvemos los datos del producto en formato JSON.
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    })



# -----------------------------
# CREAR UN PRODUCTO
# -----------------------------

# Esta ruta responde a peticiones POST en:
# /api/products
@product_controller.route('/api/products', methods=['POST'])
def create_product():

    print("Creando Producto")

    # Aquí leemos la información que envía el cliente en formato JSON.
    data = request.json

    # Creamos un nuevo producto usando los datos enviados.
    new_product = Products(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )

    # Agregamos el nuevo producto a la base de datos.
    db.session.add(new_product)

    # Guardamos los cambios definitivamente.
    db.session.commit()

    # Enviamos un mensaje indicando que el producto fue creado.
    return jsonify({'message': 'Producto creado con exito'}), 201



# -----------------------------
# ACTUALIZAR UN PRODUCTO
# -----------------------------

# Esta ruta responde a peticiones PUT en:
# /api/products/{id}
@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    # Buscamos el producto por su ID.
    product = Products.query.get_or_404(product_id)

    # Leemos el JSON enviado por el cliente.
    # silent=True evita que el servidor lance error si no viene JSON.
    data = request.get_json(silent=True) or {}

    # Aquí actualizamos SOLO los campos que vienen en el JSON.

    if "name" in data:
        product.name = data["name"]

    if "description" in data:
        product.description = data["description"]

    if "price" in data:
        product.price = data["price"]

    if "stock" in data:
        product.stock = data["stock"]

    # Guardamos los cambios en la base de datos.
    db.session.commit()

    return jsonify({"message": "Product updated successfully"}), 200



# -----------------------------
# ELIMINAR UN PRODUCTO
# -----------------------------

# Esta ruta responde a peticiones DELETE en:
# /api/products/{id}
@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):

    # Buscamos el producto por su ID.
    product = Products.query.get_or_404(product_id)

    # Eliminamos el producto de la base de datos.
    db.session.delete(product)

    # Guardamos los cambios.
    db.session.commit()

    # Enviamos un mensaje indicando que el producto fue eliminado.
    return jsonify({'message': 'Producto eliminado correctamente'})