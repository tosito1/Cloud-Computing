from dbs.db_user import (
    obtener_usuario_id,
    obtener_usuario_nombre,
    obtener_usuarios,
    insertar_usuario,
    eliminar_usuario,
    actualizar_usuario
)

# Obtiene un usuario por su nombre de usuario
def obtener_usuario_username_service(username):
    return obtener_usuario_nombre(username)

# Obtiene un usuario por su id de usuario
def obtener_usuario_id_service(user_id):
    return obtener_usuario_id(user_id)

# Obtiene todos los usuarios
def obtener_usuarios_service():
    return obtener_usuarios()

# Inserta un nuevo usuario
def insertar_usuario_service(username, password, role):
    # Puedes agregar validación aquí, por ejemplo, verificar que el usuario no existe ya
    return insertar_usuario(username, password, role)

# Elimina un usuario
def eliminar_usuario_service(username):
    user = obtener_usuario_username_service(username)
    return eliminar_usuario(user[0])

# Actualiza un usuario
def actualizar_usuario_service(user_id, username, password):
    return actualizar_usuario(user_id, username, password)
