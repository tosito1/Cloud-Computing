from dbs.db_interface import conectar, cerrar

# Crear Cuota
def insertar_cuota(user_id, monto, fecha):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO cuotas (user_id, monto, fecha) VALUES (?, ?, ?)', (user_id, monto, fecha))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar cuota: {e}")
        finally:
            cerrar(conn)

# Crear Multa
def insertar_multa(user_id, monto, fecha):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO multas (user_id, monto, fecha) VALUES (?, ?, ?)', (user_id, monto, fecha))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar multa: {e}")
        finally:
            cerrar(conn)

# Leer Cuotas
def obtener_cuotas():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cuotas')
            cuotas = cursor.fetchall()
            return cuotas
        except Exception as e:
            print(f"Error al obtener cuotas: {e}")
        finally:
            cerrar(conn)

# Leer Multas
def obtener_multas():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM multas')
            multas = cursor.fetchall()
            return multas
        except Exception as e:
            print(f"Error al obtener multas: {e}")
        finally:
            cerrar(conn)

# Actualizar Cuota
def actualizar_cuota(cuota_id, monto, fecha):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE cuotas SET monto = ?, fecha = ? WHERE id = ?', (monto, fecha, cuota_id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar cuota: {e}")
        finally:
            cerrar(conn)

# Eliminar Cuota
def eliminar_cuota(cuota_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cuotas WHERE id = ?', (cuota_id,))
            conn.commit()
        except Exception as e:
            print(f"Error al eliminar cuota: {e}")
        finally:
            cerrar(conn)
