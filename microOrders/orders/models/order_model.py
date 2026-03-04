# Importamos "db", que es el objeto de SQLAlchemy.
# SQLAlchemy es una librería que nos deja trabajar con la base de datos
# usando clases en Python en vez de escribir SQL a mano.
from db.db import db

# Importamos datetime para poder guardar la fecha y hora
# en la que se crea una orden.
from datetime import datetime


# -----------------------------
# TABLA: orders
# -----------------------------
# Esta clase representa una tabla en la base de datos.
# Cada "Order" es una orden de compra.
class Order(db.Model):

    # Nombre real de la tabla en la base de datos.
    __tablename__ = "orders"

    # Columna id:
    # - Es un número entero
    # - Es la llave principal (primary_key=True): identifica la orden de forma única
    # - Se incrementa sola (autoincrement=True): 1, 2, 3, 4...
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Nombre del usuario que hizo la compra.
    # String(255) significa texto de máximo 255 caracteres.
    # nullable=False significa que NO puede quedar vacío.
    user_name = db.Column(db.String(255), nullable=False)

    # Correo del usuario que hizo la compra.
    user_email = db.Column(db.String(255), nullable=False)

    # Total de la orden (precio final).
    # Numeric(10,2) significa número con decimales,
    # por ejemplo 12345678.90
    total = db.Column(db.Numeric(10, 2), nullable=False)

    # Fecha en la que se creó la orden.
    # default=datetime.utcnow significa que por defecto pone
    # la fecha/hora actual (en UTC) cuando se crea.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # -----------------------------------------
    # RELACIÓN: una orden tiene MUCHOS items
    # -----------------------------------------
    # Esto conecta Order con OrderItem.
    # Es decir: una orden puede tener varios productos.
    items = db.relationship(

        # Nombre del modelo con el que se relaciona
        "OrderItem",

        # backref="order" significa que desde un item también
        # puedo acceder a su orden usando item.order
        backref="order",

        # lazy=True significa que los items se cargan cuando se necesiten
        # (para no cargar todo de una).
        lazy=True,

        # cascade="all, delete-orphan":
        # - si se borra una orden, también se borran sus items
        # - y no deja items "huérfanos" sin orden.
        cascade="all, delete-orphan"
    )


    # Este es el constructor.
    # Sirve para crear una nueva orden más fácil.
    # Ejemplo:
    # order = Order(user_name="Carlos", user_email="carlos@email.com", total=100)
    def __init__(self, user_name, user_email, total):
        self.user_name = user_name
        self.user_email = user_email
        self.total = total



# -----------------------------
# TABLA: order_items
# -----------------------------
# Esta clase representa los productos dentro de una orden.
# Cada OrderItem es como una fila que dice:
# - qué producto fue
# - cuántas unidades
# - a qué precio
class OrderItem(db.Model):

    # Nombre real de la tabla en la base de datos.
    __tablename__ = "order_items"

    # ID único del item.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # order_id conecta este item con una orden.
    # ForeignKey("orders.id") significa:
    # "este campo apunta al id de la tabla orders".
    # ondelete="CASCADE" significa:
    # si se borra la orden, se borran estos items automáticamente.
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    # ID del producto (viene del microservicio de productos).
    # Aquí SOLO guardas el número del producto, no toda la info del producto.
    product_id = db.Column(db.Integer, nullable=False)

    # Cantidad comprada de ese producto.
    quantity = db.Column(db.Integer, nullable=False)

    # Precio del producto en el momento de la compra.
    # Esto es importante porque el precio puede cambiar en el futuro,
    # pero la orden debe guardar el precio con el que se compró.
    price = db.Column(db.Numeric(10, 2), nullable=False)


    # Constructor para crear un item más fácil.
    # Ejemplo:
    # item = OrderItem(order_id=1, product_id=10, quantity=2, price=25.50)
    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price