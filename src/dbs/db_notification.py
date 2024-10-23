from dbs.db_interface import conectar, cerrar

# Crear
def insertar_notificacion(titulo, mensaje, presidente_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notifications (titulo, mensaje, presidente_id) VALUES (?, ?, ?)', (titulo, mensaje, presidente_id))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar notificación: {e}")
        finally:
            cerrar(conn)

# Leer
def obtener_notificaciones():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notifications')
            notificaciones = cursor.fetchall()
            return notificaciones
        except Exception as e:
            print(f"Error al obtener notificaciones: {e}")
        finally:
            cerrar(conn)

# Actualizar
def actualizar_notificacion(notificacion_id, titulo, mensaje):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE notifications SET titulo = ?, mensaje = ? WHERE id = ?', (titulo, mensaje, notificacion_id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar notificación: {e}")
        finally:
            cerrar(conn)

# Eliminar
def eliminar_notificacion(notificacion_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notificacions WHERE id = ?', (notificacion_id,))
            conn.commit()
        except Exception as e:
            print(f"Error al eliminar notificación: {e}")
        finally:
            cerrar(conn)
