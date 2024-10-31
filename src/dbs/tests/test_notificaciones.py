import pytest
from app import app  

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            from db_interface import Base
            from sqlalchemy import create_engine
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            Base.metadata.create_all(engine)

            yield client

def test_obtener_notificaciones(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 
        
    response = client.get('/notificaciones')
    
    assert response.status_code == 200

def test_crear_notificacion(client):
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/notificaciones', data={
        'titulo': 'Título de prueba',
        'texto': 'Contenido de la notificación'
    }, follow_redirects=True)

    assert response.status_code == 200
