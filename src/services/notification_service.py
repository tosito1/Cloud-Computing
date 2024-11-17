from dbs.db_notification import (
    insertar_notificacion,
    obtener_notificaciones,
    eliminar_notificacion_db,
    actualizar_notificacion
)

# Inserta una nueva notificación
def insertar_notificacion_service(titulo, texto, user_id, fecha):
    return insertar_notificacion(titulo, texto, user_id, fecha)

# Obtiene todas las notificaciones
def obtener_notificaciones_service():
    return obtener_notificaciones()

# Elimina una notificación
def eliminar_notificacion_service(notificacion_id):
    return eliminar_notificacion_db(notificacion_id)

# Actualiza los detalles de una notificación
def actualizar_notificacion_service(notificacion_id, titulo, texto):
    return actualizar_notificacion(notificacion_id, titulo, texto)
