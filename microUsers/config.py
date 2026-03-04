# Esta clase llamada Config se usa para guardar configuraciones
# que necesita la aplicación para funcionar correctamente.
class Config:

    # SECRET_KEY es una clave secreta que usa Flask para manejar sesiones.
    # Las sesiones sirven para que el servidor recuerde quién es el usuario
    # que inició sesión.
    # Es importante para la seguridad de la aplicación.
    SECRET_KEY = "super-secret-key-dev"   # <-- NECESARIO PARA SESSION


    # MYSQL_HOST indica dónde está la base de datos.
    # En este caso "mysqlUsuarios" es el nombre del contenedor de MySQL
    # dentro de Docker donde se guardan los usuarios.
    MYSQL_HOST = "mysqlUsuarios"          # <- clave en Docker


    # MYSQL_USER es el usuario con el que la aplicación se conectará
    # a la base de datos.
    MYSQL_USER = "root"


    # MYSQL_PASSWORD es la contraseña de ese usuario.
    MYSQL_PASSWORD = "root"


    # MYSQL_DB es el nombre de la base de datos que vamos a usar.
    # En este caso la base de datos se llama "usuarios".
    MYSQL_DB = "usuarios"



    # Aquí se construye la dirección completa para conectarse a la base de datos.
    # Esto se llama URI de conexión.
    #
    # SQLAlchemy (la librería que usa Python para trabajar con bases de datos)
    # necesita esta dirección para saber:
    # - qué tipo de base de datos usar (mysql)
    # - qué usuario usar
    # - cuál es la contraseña
    # - en qué servidor está la base de datos
    # - cuál es el nombre de la base de datos
    #
    # La estructura es:
    # mysql+pymysql://usuario:password@servidor/nombre_base_datos
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )



    # Esta opción desactiva un sistema interno de SQLAlchemy
    # que detecta cambios en los objetos.
    #
    # Normalmente se desactiva porque consume recursos del servidor
    # y no es necesario para la mayoría de aplicaciones.
    SQLALCHEMY_TRACK_MODIFICATIONS = False