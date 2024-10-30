import pytest
import sqlite3

def crear_tablas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    conn.commit()

def agregar_usuario(conn, usuario):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    """, (usuario['username'], usuario['password'], usuario['role']))
    conn.commit()

def obtener_usuario(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def eliminar_usuario(conn, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()

@pytest.fixture(scope='module')
def setup_database():
    # Crear una conexión en memoria
    conn = sqlite3.connect(":memory:")
    crear_tablas(conn)  # Asegúrate de que esta función crea las tablas necesarias
    yield conn
    conn.close()

def test_agregar_usuario(setup_database):
    conn = setup_database
    usuario = {'username': 'test_user', 'password': 'test_password', 'role': 'socio'}

    # Agregar un usuario
    agregar_usuario(conn, usuario)
    
    # Verificar que el usuario fue agregado
    result = obtener_usuario(conn, 'test_user')
    assert result is not None
    assert result[1] == 'test_user'
    assert result[2] == 'test_password'
    assert result[3] == 'socio'

def test_eliminar_usuario(setup_database):
    conn = setup_database
    # Eliminar el usuario que acabamos de agregar
    eliminar_usuario(conn, 'test_user')
    
    # Verificar que el usuario fue eliminado
    result = obtener_usuario(conn, 'test_user')
    assert result is None
