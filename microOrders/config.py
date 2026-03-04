# Aquí se crea una clase llamada Config.
# Una clase en Python es como una "caja" donde guardamos configuraciones
# que luego usará nuestra aplicación.
class Config:

    # SECRET_KEY es una clave secreta que usa Flask para manejar sesiones.
    # Las sesiones permiten que el servidor recuerde quién es el usuario
    # que inició sesión.
    # En otras palabras: ayuda a mantener la seguridad cuando alguien se loguea.
    SECRET_KEY = "super-secret-key-dev"   # <-- NECESARIO PARA SESSION
    

    # MYSQL_HOST indica en qué servidor está la base de datos.
    # En este caso "mysqlOrdenes" es el nombre del contenedor de MySQL en Docker.
    MYSQL_HOST = "mysqlOrdenes"          


    # MYSQL_USER es el usuario con el que la aplicación se conecta
    # a la base de datos MySQL.
    MYSQL_USER = "root"


    # MYSQL_PASSWORD es la contraseña del usuario de la base de datos.
    MYSQL_PASSWORD = "root"


    # MYSQL_DB es el nombre de la base de datos que se va a usar.
    # En este caso la base de datos se llama "ordenes".
    MYSQL_DB = "ordenes"


    # Aquí se crea la dirección completa para conectarse a la base de datos.
    # Esto se llama URI de conexión.
    # SQLAlchemy (la librería que maneja la base de datos) necesita
    # esta dirección para saber cómo conectarse.
    #
    # La estructura es:
    # mysql+pymysql://usuario:password@servidor/nombre_base_datos
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )


    # Esta opción desactiva un sistema interno de SQLAlchemy
    # que detecta cambios en los objetos.
    # Se desactiva porque consume recursos y normalmente no se necesita.
    SQLALCHEMY_TRACK_MODIFICATIONS = False