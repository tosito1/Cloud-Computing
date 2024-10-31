import pytest
from app import app  

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123'  
    app.config['TESTING'] = True     
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'user_test',  
        'password': 'password_test', 
        'role': 'socio'
    }, follow_redirects=True)

    assert response.status_code == 200

def test_login_success(client):
    response = client.post('/login', data={
        'username': 'user_test',  
        'password': 'password_test'  
    }, follow_redirects=False)  
    
    assert response.status_code == 302  
    assert response.location == '/index'  

    
    assert response.status_code == 302  

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong_password'  
    })
    
    assert response.status_code == 200 