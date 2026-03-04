# Importamos herramientas de Flask.
# Blueprint se usa para organizar las rutas en archivos separados.
# request permite leer información que envía el cliente (por ejemplo JSON).
# jsonify convierte datos de Python a JSON para enviarlos como respuesta.
# session permite guardar información del usuario que inició sesión.
from flask import Blueprint, request, jsonify, session

# Importamos el modelo de usuarios.
# Este modelo representa la tabla de usuarios en la base de datos.
from users.models.user_model import Users

# Importamos la conexión a la base de datos.
# db permite guardar, actualizar o eliminar información en MySQL.
from db.db import db


# Creamos un Blueprint llamado user_controller.
# Esto agrupa todas las rutas relacionadas con usuarios.
user_controller = Blueprint('user_controller', __name__)



# -----------------------------------
# OBTENER TODOS LOS USUARIOS
# -----------------------------------

# Esta ruta responde a peticiones GET en:
# /api/users
@user_controller.route('/api/users', methods=['GET'])
def get_users():

    # Este mensaje se muestra en la consola del servidor.
    print("listado de usuarios")

    # Aquí consultamos todos los usuarios en la base de datos.
    users = Users.query.all()

    # Convertimos cada usuario a formato JSON para enviarlo al cliente.
    result = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'username': user.username
        }
        for user in users
    ]

    # Devolvemos la lista de usuarios.
    return jsonify(result)



# -----------------------------------
# OBTENER UN USUARIO POR ID
# -----------------------------------

# Esta ruta responde a peticiones GET en:
# /api/users/{id}
@user_controller.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    print("obteniendo usuario")

    # Buscamos el usuario por su ID.
    # Si no existe, Flask devuelve automáticamente error 404.
    user = Users.query.get_or_404(user_id)

    # Devolvemos los datos del usuario en formato JSON.
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'username': user.username
    })



# -----------------------------------
# CREAR UN USUARIO
# -----------------------------------

# Esta ruta responde a peticiones POST en:
# /api/users
@user_controller.route('/api/users', methods=['POST'])
def create_user():

    print("creando usuario")

    # Leemos los datos enviados por el cliente en formato JSON.
    data = request.json

    # Creamos un nuevo usuario usando los datos recibidos.
    new_user = Users(
        name=data['name'],
        email=data['email'],
        username=data['username'],
        password=data['password']
    )

    # Agregamos el nuevo usuario a la base de datos.
    db.session.add(new_user)

    # Guardamos los cambios definitivamente.
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201



# -----------------------------------
# ACTUALIZAR UN USUARIO
# -----------------------------------

# Esta ruta responde a peticiones PUT en:
# /api/users/{id}
@user_controller.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    print("actualizando usuario")

    # Buscamos el usuario en la base de datos.
    user = Users.query.get_or_404(user_id)

    # Leemos los datos enviados por el cliente.
    data = request.json

    # Actualizamos la información del usuario.
    user.name = data['name']
    user.email = data['email']
    user.username = data['username']
    user.password = data['password']

    # Guardamos los cambios en la base de datos.
    db.session.commit()

    return jsonify({'message': 'User updated successfully'})



# -----------------------------------
# ELIMINAR UN USUARIO
# -----------------------------------

# Esta ruta responde a peticiones DELETE en:
# /api/users/{id}
@user_controller.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    # Buscamos el usuario en la base de datos.
    user = Users.query.get_or_404(user_id)

    # Eliminamos el usuario.
    db.session.delete(user)

    # Guardamos los cambios.
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})



# -----------------------------------
# LOGIN (INICIAR SESIÓN)
# -----------------------------------

# Esta ruta permite que un usuario inicie sesión.
# Responde a peticiones POST en:
# /api/login
@user_controller.route('/api/login', methods=['POST'])
def login():

    # Leemos los datos enviados por el cliente.
    data = request.json

    # Obtenemos el username y password enviados.
    username = data.get("username")
    password = data.get("password")

    # Verificamos que ambos datos existan.
    if not username or not password:
        return jsonify({"message": "Username y password requeridos"}), 400


    # Buscamos el usuario en la base de datos.
    user = Users.query.filter_by(username=username).first()

    # Si el usuario no existe o la contraseña no coincide,
    # devolvemos error.
    if not user or user.password != password:
        return jsonify({"message": "Credenciales inválidas"}), 401


    # Si todo está correcto, creamos una sesión.
    # Esto guarda información del usuario en el servidor.
    session["username"] = user.username
    session["email"] = user.email

    return jsonify({
        "message": "Login exitoso",
        "username": user.username,
        "email": user.email
    }), 200



# -----------------------------------
# LOGOUT (CERRAR SESIÓN)
# -----------------------------------

# Esta ruta responde a:
# POST /api/logout
@user_controller.route('/api/logout', methods=['POST'])
def logout():

    # session.clear() borra toda la información de la sesión.
    # Es decir, el usuario deja de estar logueado.
    session.clear()

    return jsonify({"message": "Logout exitoso"}), 200



# -----------------------------------
# VER SESIÓN ACTUAL
# -----------------------------------

# Esta ruta sirve para comprobar si un usuario está logueado.
# GET /api/session
@user_controller.route('/api/session', methods=['GET'])
def get_session():

    # Si existe username en la sesión, significa que hay un usuario logueado.
    if "username" in session:

        return jsonify({
            "username": session["username"],
            "email": session["email"]
        }), 200

    # Si no hay sesión activa devolvemos error.
    return jsonify({"message": "No hay sesión activa"}), 401