# Importamos "db", que es el objeto de SQLAlchemy.
# SQLAlchemy es una librería que permite trabajar con la base de datos
# usando clases de Python en lugar de escribir SQL directamente.
from db.db import db


# Esta clase llamada Users representa una tabla en la base de datos.
# Cada objeto de esta clase será una fila en la tabla "users".
class Users(db.Model):

    # id es el identificador único del usuario.
    # primary_key=True significa que este campo identifica al usuario
    # de forma única dentro de la tabla.
    id = db.Column(db.Integer, primary_key=True)


    # name guarda el nombre del usuario.
    # db.String(100) significa que es un texto de máximo 100 caracteres.
    # nullable=False significa que este campo es obligatorio.
    name = db.Column(db.String(100), nullable=False)


    # email guarda el correo electrónico del usuario.
    # unique=True significa que no pueden existir dos usuarios
    # con el mismo email.
    # nullable=False significa que el email es obligatorio.
    email = db.Column(db.String(100), unique=True, nullable=False)


    # username es el nombre de usuario que la persona usará para iniciar sesión.
    # unique=True significa que cada username debe ser único.
    username = db.Column(db.String(100), unique=True, nullable=False)


    # password guarda la contraseña del usuario.
    # En este caso se guarda como texto (aunque normalmente
    # en aplicaciones reales se guarda en forma cifrada).
    password = db.Column(db.String(100), nullable=False)



    # Este es el constructor de la clase.
    # Sirve para crear usuarios de forma más fácil cuando el programa
    # necesita agregar un nuevo usuario a la base de datos.
    #
    # Ejemplo de uso:
    # user = Users("Carlos", "carlos@email.com", "cgarzon", "123456")
    def __init__(self, name, email, username, password):

        # Aquí guardamos los valores que recibe el constructor
        # dentro del objeto usuario.
        self.name = name
        self.email = email
        self.username = username
        self.password = password