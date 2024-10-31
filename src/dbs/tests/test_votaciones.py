import pytest
from flask import session
from src.app import app  # Importa tu aplicación Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Activa el modo de testing
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_obtener_votaciones(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba
    
    # Inserta una votación de prueba en la base de datos para verificar que aparece en el HTML
    #insertar_votacion('Votación Test', 'Opción 1, Opción 2')  # Ajusta los parámetros según tu lógica
    
    # Envía una solicitud GET a la página de votaciones
    response = client.get('/votaciones')
    
    # Verifica que el estado de la respuesta sea 200 (carga correcta de la página)
    assert response.status_code == 200

    # Verifica que el contenido HTML contiene la votación creada
    #assert b'Votacion Test' in response.data

def test_crear_votacion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba

    # Envía una solicitud POST para crear una nueva votación
    response = client.post('/votaciones', data={
        'titulo': 'Votación Test',
        'opciones': 'Opción 1, Opción 2'
    }, follow_redirects=True)  # Redirigir automáticamente

    # Verifica que la respuesta tenga éxito
    assert response.status_code == 200

    # Verifica que el mensaje de éxito esté presente
    #assert b'Votacion creada con exito' in response.data
def test_eliminar_votacion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba

    # Inserta una votación de prueba en la base de datos para poder eliminarla
    #insertar_votacion('Votación para Eliminar', 'Opción 1')  # Ajusta los parámetros según tu lógica

    # Encuentra el ID de la votación que acabas de crear
    #votacion_id = obtener_votacion_id_por_titulo('Votación para Eliminar')  # Asegúrate de tener esta función

    # Envía una solicitud POST para eliminar la votación
    response = client.post(f'/votaciones/{1}/eliminar', follow_redirects=True)

    # Verifica que la respuesta tenga éxito
    assert response.status_code == 200

    # Verifica que el mensaje de éxito esté presente
    #assert b'Votacion eliminada con exito' in response.data
def test_votar_opcion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba

    # Inserta una votación y opción de prueba en la base de datos
    #insertar_votacion('Votación Test', 'Opción 1, Opción 2')
    #opcion_id = obtener_opcion_id_por_votacion('Votación Test', 'Opción 1')  # Asegúrate de tener esta función

    # Envía una solicitud POST para votar
    response = client.post(f'/votaciones/votar/{1}', follow_redirects=True)

    # Verifica que la respuesta tenga éxito
    assert response.status_code == 200

    # Verifica que el mensaje de éxito esté presente
    #assert b'Voto registrado con exito.' in response.data
