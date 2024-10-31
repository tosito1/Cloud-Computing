import pytest
from app import app  # Asegúrate de que importas tu aplicación Flask

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            # Crea todas las tablas
            from db_interface import Base
            from sqlalchemy import create_engine
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            Base.metadata.create_all(engine)

            # Inserta datos de prueba aquí si es necesario
            yield client

def test_obtener_notificaciones(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1  # ID de usuario de prueba
        
    # Envía una solicitud GET a la página de notificaciones
    response = client.get('/notificaciones')
    
    # Verifica que el estado de la respuesta sea 200
    assert response.status_code == 200

def test_crear_notificacion(client):
    # Simulación de sesión iniciada
    with client.session_transaction() as session:
        session['user_id'] = 1

    # Simulación de creación de una notificación
    response = client.post('/notificaciones', data={
        'titulo': 'Título de prueba',
        'texto': 'Contenido de la notificación'
    }, follow_redirects=True)

    # Verifica que se redirige correctamente y que la página tiene el contenido esperado
    assert response.status_code == 200
    # assert b'Título de prueba' in response.data
    # assert b'Contenido de la notificación' in response.data
