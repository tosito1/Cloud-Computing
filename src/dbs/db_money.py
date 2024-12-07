import datetime
from colorama import Fore
from dbs.db_interface import conectar, cerrar

# Crear Cuota
def insertar_cuota(user_id, quota_name, amount, path_db = 'Paquito Flores.db',fine_amount=None):
    if user_id is None or not quota_name or amount <= 0:
        raise ValueError(Fore.RED + "Datos inválidos para insertar cuota.")
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            # Inserta la cuota
            cursor.execute('''
                INSERT INTO cuotas (user_id, name, amount, date, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, quota_name, amount, datetime.datetime.utcnow(), 'pagada'))
            
            quota_id = cursor.lastrowid  # Obtener el ID de la cuota recién insertada
            print(Fore.GREEN + "Cuota insertada correctamente.")

            # Si hay un monto de multa, inserta la multa y asóciala a la cuota
            if fine_amount:
                cursor.execute('''
                    INSERT INTO multas (user_id, amount, quota_id, date)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, fine_amount, quota_id, datetime.datetime.utcnow()))
                print(Fore.GREEN + "Multa insertada correctamente.")

            conn.commit()  # Guardar los cambios
            return True
        except Exception as e:
            print(Fore.RED + f"Error al registrar la cuota: {e}")
            return False
        finally:
            cerrar(conn)
    return False

# Leer Cuota por ID
def obtener_cuota_por_id(cuota_id, path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            # Ejecuta la consulta para obtener la cuota por su ID
            cursor.execute('SELECT * FROM cuotas WHERE id = ?', (cuota_id,))
            cuota = cursor.fetchone()  # Esto devuelve solo una fila
            if cuota:
                print(Fore.YELLOW + "Cuota obtenida correctamente.")
            else:
                print(Fore.YELLOW + f"No se encontró la cuota con el ID {cuota_id}.")
            return cuota  # Devuelve la cuota si se encuentra, de lo contrario None
        except Exception as e:
            print(Fore.RED + f"Error al obtener la cuota: {e}")
        finally:
            cerrar(conn)
    return None


# Crear Multa
def insertar_multa(user_id, amount, quota_id, path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO multas (user_id, amount, quota_id)
                VALUES (?, ?, ?)
            ''', (user_id, amount, quota_id))
            conn.commit()
            print(Fore.GREEN + "Multa insertada correctamente.")
            return True
        except Exception as e:
            print(Fore.RED + f"Error al registrar la multa: {e}")
            return False
        finally:
            cerrar(conn)
    return False


# Leer Cuotas
def obtener_cuotas(path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cuotas')
            cuotas = cursor.fetchall()
            print(Fore.YELLOW + "Cuota obtenida correctamente.")
            return cuotas
        except Exception as e:
            print(Fore.RED + f"Error al obtener cuotas: {e}")
        finally:
            cerrar(conn)

# Leer Multas
def obtener_multas(path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM multas')
            multas = cursor.fetchall()
            print(Fore.YELLOW + "Multa obtenida correctamente.")
            return multas
        except Exception as e:
            print(Fore.RED + f"Error al obtener multas: {e}")
        finally:
            cerrar(conn)

# Actualizar Cuota
# def actualizar_cuota(cuota_id, monto, fecha, path_db = 'Paquito Flores.db'):
#     conn = conectar(path_db)
#     if conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute('UPDATE cuotas SET monto = ?, fecha = ? WHERE id = ?', (monto, fecha, cuota_id))
#             conn.commit()
#         except Exception as e:
#             print(f"Error al actualizar cuota: {e}")
#         finally:
#             cerrar(conn)

# Eliminar Cuota
def eliminar_cuota(cuota_id, path_db = 'Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cuotas WHERE id = ?', (cuota_id,))
            conn.commit()
            print(Fore.GREEN + "Cuota Eliminada correctamente.")
        except Exception as e:
            print(Fore.RED + f"Error al eliminar cuota: {e}")
        finally:
            cerrar(conn)
