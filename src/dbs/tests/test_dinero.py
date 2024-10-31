import pytest
from app import app  

@pytest.fixture
def client():
    app.config['SECRET_KEY'] = '123' 
    app.config['TESTING'] = True      
    with app.test_client() as client:
        yield client

def test_obtener_dinero(client):
    with client.session_transaction() as session:
        session['user_id'] = 1 
        
    response = client.get('/dinero')
    
    assert response.status_code == 200

def test_registrar_pago(client):
    with client.session_transaction() as session:
        session['user_id'] = 1  

    response = client.post('/dinero', data={
        'user_id': 1,
        'amount': '150', 
        'quota_name': 'Cuota Test',  
        'multa_amount': '25'  
    }, follow_redirects=True) 

    assert response.status_code == 200