import pytest
from sqlalchemy.orm import sessionmaker
from db_interface import Base, create_database

@pytest.fixture(scope='module')
def test_database():
    engine = create_database("Paquito Flores")
    yield engine 


def test_tables_creation(test_database):
    Session = sessionmaker(bind=test_database)
    session = Session()

    assert 'users' in Base.metadata.tables  
    assert 'notificationes' in Base.metadata.tables  
    assert 'votaciones' in Base.metadata.tables 
    assert 'opciones' in Base.metadata.tables 
    assert 'votes' in Base.metadata.tables  
    assert 'cuotas' in Base.metadata.tables 
    assert 'multas' in Base.metadata.tables 

    session.close()

if __name__ == '__main__':
    pytest.main()