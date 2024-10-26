import datetime
import sqlite3
from dbs.db_interface import conectar, cerrar

# Crear
def insertar_notificacion(titulo, mensaje, presidente_id, fecha_actual):
    # Validación de entradas
    if not titulo or not mensaje or not presidente_id:
        print("Título, mensaje y presidente_id son obligatorios.")
        return

    conn = conectar()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO notificationes (title, text, president_id, date) VALUES (?, ?, ?, ?)', (titulo, mensaje, presidente_id, fecha_actual))
                print("Notificación insertada correctamente.")
        except sqlite3.IntegrityError as ie:
            print(f"Error de integridad al insertar notificación: {ie}")
        except sqlite3.Error as e:
            print(f"Error al insertar notificación: {e}")
        finally:
            cerrar(conn)
    else:
        print("No se pudo establecer la conexión a la base de datos.")

# Leer
def obtener_notificaciones():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notificationes')
            print(datetime.datetime.now)
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
            cursor.execute('UPDATE notificationes SET titulo = ?, mensaje = ? WHERE id = ?', (titulo, mensaje, notificacion_id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar notificación: {e}")
        finally:
            cerrar(conn)

# Eliminar
def eliminar_notificacion_db(notificacion_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notificationes WHERE id = ?', (notificacion_id,))
            conn.commit()
        except Exception as e:
            print(f"Error al eliminar notificación: {e}")
        finally:
            cerrar(conn)
