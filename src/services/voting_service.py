from dbs.db_voting import (
    insertar_votacion,
    obtener_votaciones,
    eliminar_votacion_db,
    actualizar_votacion,
    registrar_voto
)

# Inserta una nueva votación
def insertar_votacion_service(titulo, descripcion):
    return insertar_votacion(titulo, descripcion)

# Obtiene todas las votaciones
def obtener_votaciones_service():
    return obtener_votaciones()

# Elimina una votación por su ID
def eliminar_votacion_service(votacion_id):
    return eliminar_votacion_db(votacion_id)

# Actualiza los detalles de una votación
def actualizar_votacion_service(votacion_id, titulo, descripcion):
    return actualizar_votacion(votacion_id, titulo, descripcion)

# Registra un voto para una opción de una votación
def registrar_voto_service(opcion_id, user_id):
    return registrar_voto(opcion_id, user_id)
