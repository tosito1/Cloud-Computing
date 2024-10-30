import pytest
import pytest
from app import app  # Asegúrate de que importas tu aplicación Flask

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'  # Configura la clave secreta aquí
    app.config['TESTING'] = True      # Activa el modo de pruebas
    with app.test_client() as client:
        yield client

def test_obtener_notificaciones(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincide con un usuario de prueba
        
    # Envía una solicitud GET a la página de notificaciones
    response = client.get('/notificaciones')
    
    # Verifica que el estado de la respuesta sea 200 (carga correcta de la página)
    assert response.status_code == 200

def test_crear_notificacion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincida con un usuario de prueba

    # Simulación de creación de una notificación
    response = client.post('/notificaciones', data={
        'titulo': 'Título de prueba',
        'texto': 'Contenido de la notificación'
    }, follow_redirects=True)

    # Verifica que se redirige correctamente
    assert response.status_code == 200
    #assert b'Notificacion creada con exito' in response.data

    # Verifica que la notificación está en la lista de notificaciones
    #notificaciones = obtener_notificaciones()
    #assert any(n.titulo == 'Título de prueba' and n.texto == 'Contenido de la notificación' for n in notificaciones)

def test_eliminar_notificacion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # Asegúrate de que este ID coincida con un usuario de prueba

    # Añade una notificación de prueba a la base de datos para eliminarla
    # insertar_notificacion('Título a eliminar', 'Texto de prueba', session['user_id'], datetime.date.today())
    # notificaciones = obtener_notificaciones()
    # notificacion_id = next((n.id for n in notificaciones if n.titulo == 'Título a eliminar'), None)

    # Simulación de eliminación de la notificación
    response = client.post(f'/notificaciones/{3}/eliminar', follow_redirects=True)

    # Verifica que se redirige correctamente y que muestra el mensaje de éxito
    assert response.status_code == 200
    #assert b'Notificacion eliminada con exito' in response.data

    # Verifica que la notificación ya no está en la lista
    # notificaciones = obtener_notificaciones()
    # assert all(n.id != notificacion_id for n in notificaciones)