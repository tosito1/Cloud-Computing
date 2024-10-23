from dbs.db_interface import conectar, cerrar

# Crear Votación
def insertar_votacion(titulo, descripcion):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO votaciones (titulo, descripcion) VALUES (?, ?)', (titulo, descripcion))
            conn.commit()
            return cursor.lastrowid  # Devolver ID de la nueva votación
        except Exception as e:
            print(f"Error al insertar votación: {e}")
        finally:
            cerrar(conn)

# Crear Opciones
def insertar_opcion(votacion_id, opcion):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO opciones (votacion_id, opcion) VALUES (?, ?)', (votacion_id, opcion))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar opción: {e}")
        finally:
            cerrar(conn)

# Leer Votaciones y Opciones
def obtener_votaciones():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM votaciones')
            votaciones = cursor.fetchall()
            return votaciones
        except Exception as e:
            print(f"Error al obtener votaciones: {e}")
        finally:
            cerrar(conn)

# Actualizar Votación
def actualizar_votacion(votacion_id, titulo, descripcion):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE votaciones SET titulo = ?, descripcion = ? WHERE id = ?', (titulo, descripcion, votacion_id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar votación: {e}")
        finally:
            cerrar(conn)

# Eliminar Votación
def eliminar_votacion(votacion_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM votaciones WHERE id = ?', (votacion_id,))
            conn.commit()
        except Exception as e:
            print(f"Error al eliminar votación: {e}")
        finally:
            cerrar(conn)
