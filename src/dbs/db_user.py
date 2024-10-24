from dbs.db_interface import conectar, cerrar
import bcrypt

# Crear
def insertar_usuario(username, password, role):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
        finally:
            cerrar(conn)

# Leer
def obtener_usuarios():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')  # Selecciona todos los usuarios
            usuarios = cursor.fetchall()  # Obtén todos los resultados
            return usuarios  # Devuelve la lista de usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []  # Devuelve una lista vacía en caso de error
        finally:
            cerrar(conn)  # Asegúrate de cerrar la conexión


def obtener_usuario_por_id(user_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
        finally:
            cerrar(conn)

def obtener_usuario_por_nombre(username):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
        finally:
            cerrar(conn)

# Actualizar
def actualizar_usuario(user_id, username, password, role):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET username = ?, password_hash = ?, role = ? WHERE id = ?', (username, password, role, user_id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
        finally:
            cerrar(conn)

# Eliminar
def eliminar_usuario(user_id):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
        finally:
            cerrar(conn)

def registrar_usuario(username, password, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
    finally:
        cursor.close()
        cerrar(conn)


def usuario_existe(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def verificar_contrasena(password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con la contraseña hasheada."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
