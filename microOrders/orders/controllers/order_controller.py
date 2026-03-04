# Importamos herramientas de Flask.
# Blueprint permite organizar rutas en archivos separados.
# request permite leer datos enviados por el cliente.
# jsonify convierte datos de Python a JSON (formato que usan las APIs).
# session permite leer información guardada del usuario logueado.
from flask import Blueprint, request, jsonify, session

# Importamos los modelos de base de datos.
# Order representa la tabla de órdenes.
# OrderItem representa los productos dentro de cada orden.
from orders.models.order_model import Order, OrderItem

# Importamos la conexión a la base de datos.
from db.db import db

# Importamos requests para poder llamar a otros microservicios.
import requests


# Creamos un Blueprint llamado order_controller.
# Esto permite agrupar todas las rutas relacionadas con órdenes.
order_controller = Blueprint('order_controller', __name__)



# -------------------------------------------
# FUNCIÓN PARA ENCONTRAR EL MICROSERVICIO DE PRODUCTOS
# -------------------------------------------

# Esta función busca el microservicio de productos usando Consul.
# Consul es una herramienta que permite que los servicios se descubran entre sí.
def get_products_service_url():

    # Hacemos una petición a Consul para preguntar
    # dónde está el servicio llamado "micro_products".
    resp = requests.get(
        "http://consul:8500/v1/health/service/micro_products?passing=true",
        timeout=5
    )

    # Convertimos la respuesta a formato JSON.
    services = resp.json()

    # Si no hay servicios disponibles devolvemos None.
    if not services:
        return None

    # Tomamos el primer servicio encontrado.
    svc = services[0]["Service"]

    # Construimos la URL completa del microservicio de productos.
    return f"http://{svc['Address']}:{svc['Port']}"



# -------------------------------------------
# OBTENER TODAS LAS ÓRDENES
# -------------------------------------------

@order_controller.route('/api/orders', methods=['GET'])
def get_all_orders():
    try:

        # Consultamos todas las órdenes de la base de datos.
        # order_by(Order.id.desc()) las ordena de más nueva a más vieja.
        orders = Order.query.order_by(Order.id.desc()).all()

        # Aquí guardaremos las órdenes convertidas a JSON.
        result = []

        # Recorremos cada orden.
        for o in orders:

            # Convertimos la orden a un diccionario.
            result.append({
                "id": o.id,
                "user_name": o.user_name,
                "user_email": o.user_email,
                "total": float(o.total),

                # Convertimos la fecha a texto.
                "created_at": o.created_at.isoformat() if o.created_at else None,

                # Aquí agregamos los productos de la orden.
                "items": [
                    {
                        "id": it.id,
                        "product_id": it.product_id,
                        "quantity": it.quantity,
                        "price": float(it.price),
                    } for it in (o.items or [])
                ]
            })

        # Devolvemos todas las órdenes en formato JSON.
        return jsonify(result), 200

    except Exception as e:
        # Si ocurre un error devolvemos un mensaje de error.
        return jsonify({"message": "Error interno", "error": str(e)}), 500



# -------------------------------------------
# OBTENER UNA ORDEN ESPECÍFICA
# -------------------------------------------

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:

        # Buscamos la orden por su ID.
        # Si no existe devuelve error 404 automáticamente.
        order = Order.query.get_or_404(order_id)

        # Construimos el JSON de respuesta.
        payload = {
            "id": order.id,
            "user_name": order.user_name,
            "user_email": order.user_email,
            "total": float(order.total),
            "created_at": order.created_at.isoformat() if order.created_at else None,

            # Lista de productos de la orden.
            "items": [
                {
                    "id": it.id,
                    "product_id": it.product_id,
                    "quantity": it.quantity,
                    "price": float(it.price),
                } for it in (order.items or [])
            ]
        }

        return jsonify(payload), 200

    except Exception as e:
        return jsonify({"message": "Error interno", "error": str(e)}), 500



# -------------------------------------------
# CREAR UNA NUEVA ORDEN
# -------------------------------------------

@order_controller.route('/api/orders', methods=['POST'])
def create_order():

    """
    Este endpoint crea una nueva orden de compra.
    El cliente envía una lista de productos con cantidades.
    El sistema calcula el total, verifica el inventario
    y guarda la orden en la base de datos.
    """

    try:

        # Leemos el JSON que envía el cliente.
        data = request.get_json(silent=True) or {}



        # -----------------------------------
        # 1) OBTENER USUARIO DESDE LA SESIÓN
        # -----------------------------------

        # El usuario que inició sesión está guardado en session.
        user_name = session.get('username')
        user_email = session.get('email')

        # Si no existe usuario en sesión devolvemos error.
        if not user_name or not user_email:
            return jsonify({'message': 'Información de usuario inválida'}), 400



        # -----------------------------------
        # 2) VALIDAR LISTA DE PRODUCTOS
        # -----------------------------------

        products = data.get('products')

        # Verificamos que exista una lista de productos.
        if not products or not isinstance(products, list):
            return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400


        # Validamos cada producto.
        for p in products:

            if not isinstance(p, dict):
                return jsonify({'message': 'Formato inválido en products'}), 400

            if 'id' not in p or 'quantity' not in p:
                return jsonify({'message': 'Cada producto debe incluir id y quantity'}), 400

            if not isinstance(p['id'], int) or not isinstance(p['quantity'], int):
                return jsonify({'message': 'id y quantity deben ser enteros'}), 400

            if p['quantity'] <= 0:
                return jsonify({'message': 'quantity debe ser mayor a 0'}), 400



        # -----------------------------------
        # 3) ENCONTRAR MICROSERVICIO PRODUCTS
        # -----------------------------------

        products_url = get_products_service_url()

        if not products_url:
            return jsonify({"message": "Products no disponible (Consul)"}), 500



        # -----------------------------------
        # 4) CONSULTAR PRODUCTOS
        # -----------------------------------

        order_items_data = []
        total = 0.0

        for p in products:

            product_id = p['id']
            qty = p['quantity']

            # Pedimos información del producto al microservicio de productos.
            resp = requests.get(f"{products_url}/api/products/{product_id}", timeout=5)

            if resp.status_code == 404:
                return jsonify({'message': f'Producto no existe: {product_id}'}), 404

            if resp.status_code != 200:
                return jsonify({'message': 'Error consultando productos'}), 500

            prod = resp.json()

            stock = prod.get("stock")
            price = prod.get("price")

            # Validamos la respuesta.
            if stock is None or price is None:
                return jsonify({'message': 'Respuesta inválida del servicio de productos'}), 500

            # Verificamos si hay suficiente inventario.
            if int(stock) < qty:
                return jsonify({'message': f'Inventario insuficiente para producto {product_id}'}), 409

            # Calculamos el total.
            price_f = float(price)
            total += price_f * qty

            order_items_data.append({
                "product_id": product_id,
                "quantity": qty,
                "price": price_f
            })



        # -----------------------------------
        # 5) ACTUALIZAR INVENTARIO
        # -----------------------------------

        for it in order_items_data:

            product_id = it["product_id"]
            qty = it["quantity"]

            # Consultamos nuevamente el stock actual.
            resp = requests.get(f"{products_url}/api/products/{product_id}", timeout=5)

            if resp.status_code != 200:
                return jsonify({'message': 'Error validando inventario (re-check)'}), 500

            prod = resp.json()
            current_stock = int(prod.get("stock", 0))

            # Calculamos el nuevo stock.
            new_stock = current_stock - qty

            payload_update = {"stock": new_stock}

            # Actualizamos el producto en el microservicio de productos.
            upd = requests.put(
                f"{products_url}/api/products/{product_id}",
                json=payload_update,
                timeout=5
            )

            if upd.status_code == 404:
                return jsonify({'message': f'Producto no existe: {product_id}'}), 404

            if upd.status_code not in (200, 204):
                return jsonify({'message': f'Error actualizando inventario para producto {product_id}'}), 500



        # -----------------------------------
        # 6) GUARDAR ORDEN EN BASE DE DATOS
        # -----------------------------------

        order = Order(user_name=user_name, user_email=user_email, total=total)

        db.session.add(order)

        # flush permite obtener el ID antes de hacer commit.
        db.session.flush()

        # Guardamos cada producto de la orden.
        for it in order_items_data:

            item = OrderItem(
                order_id=order.id,
                product_id=it["product_id"],
                quantity=it["quantity"],
                price=it["price"]
            )

            db.session.add(item)

        # Guardamos definitivamente en la base de datos.
        db.session.commit()

        return jsonify({'message': 'Orden creada exitosamente', 'order_id': order.id}), 201



    # -----------------------------------
    # MANEJO DE ERRORES
    # -----------------------------------

    except requests.exceptions.Timeout:
        return jsonify({'message': 'Timeout consultando servicio de productos'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Error llamando al servicio de productos', 'error': str(e)}), 500

    except Exception as e:

        # Si ocurre un error revertimos los cambios en la base de datos.
        db.session.rollback()

        return jsonify({'message': 'Error interno', 'error': str(e)}), 500