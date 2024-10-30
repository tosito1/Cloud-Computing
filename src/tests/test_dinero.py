import pytest
import pytest
from app import app  # Asegúrate de que importas tu aplicación Flask

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'  # Configura la clave secreta aquí
    app.config['TESTING'] = True      # Activa el modo de pruebas
    with app.test_client() as client:
        yield client

def test_obtener_dinero(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba
    
    # Inserta cuotas y multas de prueba en la base de datos para verificar que aparecen en el HTML
    # insertar_cuota(1, 'Cuota Test', 100)  # Ajusta los parámetros según tu lógica
    # insertar_multa(50)  # Inserta una multa de prueba
    
    # Envía una solicitud GET a la página de dinero
    response = client.get('/dinero')
    
    # Verifica que el estado de la respuesta sea 200 (carga correcta de la página)
    assert response.status_code == 200

    # Verifica que el contenido HTML contiene información de la cuota y multa creadas
    # assert b'Cuota Test' in response.data
    # assert b'50' in response.data  # Verifica que la multa también está presente

def test_registrar_pago(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba

    # Envía una solicitud POST para registrar un pago
    response = client.post('/dinero', data={
        'user_id': 1,
        'amount': '150',  # Monto del pago
        'quota_name': 'Cuota Test',  # Nombre de la cuota
        'multa_amount': '25'  # Monto de la multa (opcional)
    }, follow_redirects=True)  # Redirigir automáticamente

    # Verifica que la respuesta tenga éxito
    assert response.status_code == 200

    # Verifica que el mensaje de éxito esté presente
    #assert b'Pago registrado con exito.' in response.data
