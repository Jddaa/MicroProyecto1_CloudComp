# Importamos "db", que es el objeto de SQLAlchemy.
# SQLAlchemy permite trabajar con la base de datos usando clases en Python.
from db.db import db


# Esta clase representa la tabla de productos en la base de datos.
# Cada objeto Products = 1 fila en la tabla (un producto).
class Products(db.Model):

    # id es el identificador único del producto.
    # primary_key=True significa que este campo identifica al producto de forma única.
    id = db.Column(db.Integer, primary_key=True)

    # name es el nombre del producto.
    # db.String(255) significa texto de máximo 255 caracteres.
    # nullable=False significa que este campo NO puede quedar vacío.
    name = db.Column(db.String(255), nullable=False)

    # description es la descripción del producto.
    # db.Text permite textos largos (más que 255 caracteres).
    # (Como no tiene nullable=False, puede ser opcional)
    description = db.Column(db.Text)

    # price es el precio del producto.
    # Numeric(10,2) significa:
    # - máximo 10 dígitos en total
    # - 2 de esos dígitos son decimales
    # Ejemplo: 12345678.90
    # nullable=False significa que el precio siempre debe existir.
    price = db.Column(db.Numeric(10,2), nullable=False)

    # stock es cuántas unidades hay disponibles.
    # nullable=False significa que siempre debe tener un valor.
    # default=0 significa que si no se manda stock, empieza en 0.
    stock = db.Column(db.Integer, nullable=False, default=0)


    # Este es el constructor.
    # Sirve para crear productos más fácil.
    # Ejemplo:
    # p = Products("Mouse", "Mouse gamer", 50, 20)
    def __init__(self, name, description, price, stock):

        # Guardamos los valores en el objeto.
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock