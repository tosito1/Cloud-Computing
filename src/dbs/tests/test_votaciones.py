import pytest
from flask import session
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True 
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_obtener_votaciones(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 
    
    response = client.get('/votaciones')
    
    assert response.status_code == 200

def test_crear_votacion(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 

    response = client.post('/votaciones', data={
        'titulo': 'Votación Test',
        'opciones': 'Opción 1, Opción 2'
    }, follow_redirects=True) 

    assert response.status_code == 200

def test_eliminar_votacion(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 

    response = client.post(f'/votaciones/{1}/eliminar', follow_redirects=True)

    assert response.status_code == 200

def test_votar_opcion(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 

    response = client.post(f'/votaciones/votar/{1}', follow_redirects=True)

    assert response.status_code == 200
