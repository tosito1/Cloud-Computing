from dbs.db_user import (
    obtener_usuario_por_nombre,
    verificar_contrasena
)

# Verifica las credenciales de un usuario (nombre de usuario y contraseña)
def verificar_credenciales(username, password):
    user = obtener_usuario_por_nombre(username)
    if user and verificar_contrasena(password, user[2]):
        return user
    return None
