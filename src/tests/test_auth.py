import pytest
from src.app import app  # Asegúrate de que importas tu aplicación Flask

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'  # Configura la clave secreta aquí
    app.config['TESTING'] = True      # Activa el modo de pruebas
    with app.test_client() as client:
        yield client

def test_register_user(client):
    # Datos del nuevo usuario
    response = client.post('/register', data={
        'username': 'user_test',  # Nombre de usuario nuevo
        'password': 'password_test',  # Contraseña del usuario
        'role': 'socio'
    }, follow_redirects=True)

    # Verificar que la respuesta tiene éxito y el mensaje esperado está en la respuesta
    assert response.status_code == 200
    #assert b'Usuario registrado con exito.' in response.data  # Mensaje de confirmación


def test_login_success(client):
    response = client.post('/login', data={
        'username': 'user_test',  # Usuario válido
        'password': 'password_test'  # Contraseña válida
    }, follow_redirects=False)  # No seguir redirecciones automáticamente
    
    assert response.status_code == 302  # Verifica el código de estado para redirección
    assert response.location == '/index'  # Verifica la URL de redirección esperada

    
    assert response.status_code == 302  # El código de estado para redirección

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong_password'  # Contraseña incorrecta
    })
    
    assert response.status_code == 200  # Verifica que la respuesta sea 200
    #assert b'Credenciales incorrectas.' in response.data  # Verifica que el mensaje de error esté en la respuesta
