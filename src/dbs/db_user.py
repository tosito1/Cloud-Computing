from dbs.db_interface import conectar, cerrar
import bcrypt
from colorama import Fore

# Crear
def insertar_usuario(username, password, role):
    conn = conectar('Paquito Flores.db')
    if conn:
        try:
            # Hashea la contraseña antes de guardarla
            hashed_password = hash_password(password)
            # Inserta el usuario con la contraseña hasheada
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, hashed_password, role))
            conn.commit()
        except Exception as e:
            print(Fore.RED + f"Error al insertar usuario: {e}")
        finally:
            cerrar(conn)


# Leer
def obtener_usuarios():
    conn = conectar('Paquito Flores.db')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')  # Selecciona todos los usuarios
            usuarios = cursor.fetchall()  # Obtén todos los resultados
            return usuarios  # Devuelve la lista de usuarios
        except Exception as e:
            print(Fore.RED + f"Error al obtener usuarios: {e}")
            return []  # Devuelve una lista vacía en caso de error
        finally:
            cerrar(conn)  # Asegúrate de cerrar la conexión


def obtener_usuario_id(user_id):
    conn = conectar('Paquito Flores.db')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(Fore.RED + f"Error al obtener usuario: {e}")
        finally:
            cerrar(conn)

def obtener_usuario_nombre(username, path_db='Paquito Flores.db'):
    conn = conectar(path_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()  # Esto devuelve una tupla
            if user:
                # Convierte la tupla en un diccionario
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'role': user[3]
                }
                return user_dict  # Ahora devuelve un diccionario
            return None
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            cerrar(conn)
    return None

# Actualizar
def actualizar_usuario(user_id, username, password, role):
    conn = conectar('Paquito Flores.db')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET username = ?, password_hash = ?, role = ? WHERE id = ?', (username, password, role, user_id))
            conn.commit()
        except Exception as e:
            print(Fore.RED + f"Error al actualizar usuario: {e}")
        finally:
            cerrar(conn)

# Eliminar
def eliminar_usuario(id_user):
    conn = conectar('Paquito Flores.db')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (id_user,))
            conn.commit()
        except Exception as e:
            print(Fore.RED + f"Error al eliminar usuario: {e}")
        finally:
            cerrar(conn)

def registrar_usuario(username, password, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = conectar('Paquito Flores.db')
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
    except Exception as e:
        print(Fore.RED + f"Error al registrar usuario: {e}")
    finally:
        cursor.close()
        cerrar(conn)


def usuario_existe(username):
    conn = conectar('Paquito Flores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt y retorna el hash."""
    # Generar un salt
    salt = bcrypt.gensalt()
    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verificar_contrasena(password: bytes, hashed_password: bytes) -> bool:
    """Verifica si la contraseña proporcionada coincide con la contraseña hasheada."""
    print(f"Contraseña proporcionada: {password}")
    print(f"Contraseña hasheada: {hashed_password}")
    return bcrypt.checkpw(password, hashed_password)

