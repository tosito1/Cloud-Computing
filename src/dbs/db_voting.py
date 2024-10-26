from dbs.db_interface import Voting, conectar, cerrar

# Crear Votación
def insertar_votacion(titulo, opciones_str):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            # Insertar la votación y obtener su ID
            cursor.execute('INSERT INTO votaciones (title, description) VALUES (?, ?)', (titulo, opciones_str))
            votacion_id = cursor.lastrowid  # Obtener el ID de la votación recién creada

            # Separar las opciones en un listado y guardar cada opción en la tabla de opciones
            opciones = opciones_str.split(',')  # Suponiendo que las opciones están separadas por comas
            for opcion in opciones:
                opcion_texto = opcion.strip()  # Limpiar espacios en blanco
                cursor.execute('INSERT INTO opciones (voting_id, option_text) VALUES (?, ?)', (votacion_id, opcion_texto))

            conn.commit()
            return votacion_id  # Retornar el ID de la nueva votación
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

def obtener_votaciones():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()

            # Consulta para obtener las votaciones, sus opciones y el conteo de votos por cada opción
            cursor.execute('''
                SELECT v.id, v.title, v.description, o.id AS option_id, o.option_text,
                    (SELECT COUNT(*) FROM votes WHERE option_id = o.id) AS vote_count
                FROM votaciones v
                LEFT JOIN opciones o ON v.id = o.voting_id
            ''')
            resultados = cursor.fetchall()

            # Estructura para almacenar las votaciones y sus opciones
            votaciones = {}
            for row in resultados:
                votacion_id = row[0]
                if votacion_id not in votaciones:
                    votaciones[votacion_id] = {
                        'title': row[1],
                        'description': row[2],
                        'options': []
                    }
                # Agregar opciones a la votación
                if row[3]:  # Verifica si hay una opción
                    votaciones[votacion_id]['options'].append({
                        'id': row[3],
                        'option_text': row[4],
                        'vote_count': row[5]  # Número de votos para esta opción
                    })

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
def eliminar_votacion_db(votacion_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()

            # Eliminar todos los votos asociados a la votación
            cursor.execute('DELETE FROM votes WHERE option_id IN (SELECT id FROM opciones WHERE voting_id = ?)', (votacion_id,))
            # Eliminar la votación y sus opciones
            cursor.execute('DELETE FROM opciones WHERE voting_id = ?', (votacion_id,))
            cursor.execute('DELETE FROM votaciones WHERE id = ?', (votacion_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar votación: {e}")
            return False
        finally:
            cerrar(conn)
    return False



def registrar_voto(opcion_id, user_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()

            # Verificar si el usuario ya votó en esta opción
            cursor.execute('SELECT id FROM votes WHERE user_id = ? AND option_id = ?', (user_id, opcion_id))
            if cursor.fetchone():
                return False  # Ya votó en esta opción
            
            # Insertar el voto
            cursor.execute('INSERT INTO votes (user_id, option_id) VALUES (?, ?)', (user_id, opcion_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar voto: {e}")
            return False
        finally:
            cerrar(conn)
    return False
