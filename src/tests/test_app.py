import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_greet(client):
    response = client.get('/greet?name=Test')
    assert response.data == b'Hola, Test!'

def test_build(client):
    response = client.get('/build')
    assert response.data == b'Construyendo el proyecto...'

def test_test(client):
    response = client.get('/test')
    assert response.data == b'Ejecutando pruebas...'

