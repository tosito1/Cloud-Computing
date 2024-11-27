import datetime
import sqlite3
from colorama import Fore
from dbs.db_interface import conectar, cerrar

# Crear
def insertar_notificacion(titulo, mensaje, presidente_id, fecha_actual, path_db = 'Paquito Flores.db'):
    # Validación de entradas
    if not isinstance(fecha_actual, datetime.datetime):
        raise TypeError(Fore.RED + "La fecha debe ser un objeto datetime válido.")
    if not titulo or not mensaje or not presidente_id:
        raise TypeError(Fore.RED + "Título, mensaje y presidente_id son obligatorios.")

    conn = conectar(path_db)
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO notificationes (title, text, president_id, date) VALUES (?, ?, ?, ?)', (titulo, mensaje, presidente_id, fecha_actual))
                print(Fore.GREEN + "Notificación insertada correctamente.")
        except sqlite3.IntegrityError as ie:
            print(Fore.RED + f"Error de integridad al insertar notificación: {ie}")
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al insertar notificación: {e}")
        finally:
            cerrar(conn)
    else:
        print(Fore.RED + "No se pudo establecer la conexión a la base de datos.")

# Leer
def obtener_notificaciones(path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notificationes')
            notificaciones = cursor.fetchall()
            print(Fore.YELLOW + "Notifiacion obtenida correctamente.")
            return notificaciones
        except Exception as e:
            print(Fore.RED + f"Error al obtener notificaciones: {e}")
        finally:
            cerrar(conn)

# Actualizar
def actualizar_notificacion(notificacion_id, titulo, mensaje, path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE notificationes SET titulo = ?, mensaje = ? WHERE id = ?', (titulo, mensaje, notificacion_id))
            conn.commit()
        except Exception as e:
            print(Fore.RED + f"Error al actualizar notificación: {e}")
        finally:
            cerrar(conn)

# Eliminar
def eliminar_notificacion_db(notificacion_id, path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notificationes WHERE id = ?', (notificacion_id,))
            conn.commit()
            print(Fore.GREEN + "Notificación eliminada correctamente.")
        except Exception as e:
            print(Fore.RED + f"Error al eliminar notificación: {e}")
        finally:
            cerrar(conn)
