# Aquí se crea una clase llamada Config.
# Una clase en Python se usa como un lugar para guardar configuraciones
# que la aplicación necesitará para funcionar.
class Config:


    # MYSQL_HOST indica dónde está la base de datos.
    # En este caso "mysqlProductos" es el nombre del contenedor
    # donde está corriendo MySQL dentro de Docker.
    MYSQL_HOST = "mysqlProductos"


    # MYSQL_USER es el usuario que la aplicación usará
    # para conectarse a la base de datos.
    MYSQL_USER = "root"


    # MYSQL_PASSWORD es la contraseña de ese usuario.
    MYSQL_PASSWORD = "root"


    # MYSQL_DB es el nombre de la base de datos que vamos a usar.
    # En este caso la base de datos se llama "productos".
    MYSQL_DB = "productos"



    # Aquí se crea la dirección completa para conectarse a la base de datos.
    # Esta dirección se llama URI de conexión.
    #
    # SQLAlchemy (la librería que maneja la base de datos) necesita esta
    # dirección para saber:
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
    # Normalmente se desactiva porque consume recursos
    # y no es necesario para la mayoría de aplicaciones.
    SQLALCHEMY_TRACK_MODIFICATIONS = False