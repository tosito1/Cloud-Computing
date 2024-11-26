from dbs.db_money import (
    insertar_cuota,
    obtener_cuotas,
    obtener_cuota_por_id,
    eliminar_cuota,
    #actualizar_cuota
)

# Inserta una nueva cuota o multa
def insertar_cuota_service(user_id, nombre_cuota, dinero):
    return insertar_cuota(user_id, nombre_cuota, dinero)

# Obtiene todas las cuotas o multas
def obtener_cuotas_service():
    return obtener_cuotas()

# Obtiene una cuota específica por su ID
def obtener_cuota_por_id_service(cuota_id):
    return obtener_cuota_por_id(cuota_id)

# Elimina una cuota por su ID
def eliminar_cuota_service(cuota_id):
    return eliminar_cuota(cuota_id)

# Actualiza una cuota existente
# def actualizar_cuota_service(cuota_id, monto, descripcion, fecha_vencimiento):
#     return actualizar_cuota(cuota_id, monto, descripcion, fecha_vencimiento)
