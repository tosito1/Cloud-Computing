# tests/test_db.py
import pytest
from sqlalchemy.orm import sessionmaker
from dbs.db_interface import create_database, Base

@pytest.fixture(scope='module')
def test_database():
    # Crea la base de datos de prueba y devuelve el motor
    engine = create_database("Paquito Flores")
    yield engine  # Devuelve el motor para usar en las pruebas

    # Limpia la base de datos después de todas las pruebas
    #os.remove(f'{TEST_DB_NAME}.db')

def test_tables_creation(test_database):
    Session = sessionmaker(bind=test_database)
    session = Session()

    # Verifica que cada tabla ha sido creada
    assert 'users' in Base.metadata.tables  # Verifica que la tabla User existe
    assert 'notificationes' in Base.metadata.tables  # Verifica que la tabla Notification existe
    assert 'votaciones' in Base.metadata.tables  # Verifica que la tabla Voting existe
    assert 'opciones' in Base.metadata.tables  # Verifica que la tabla Option existe
    assert 'votes' in Base.metadata.tables  # Verifica que la tabla Vote existe
    assert 'cuotas' in Base.metadata.tables  # Verifica que la tabla Quota existe
    assert 'multas' in Base.metadata.tables  # Verifica que la tabla Fine existe

    session.close()  # Cierra la sesión

if __name__ == '__main__':
    pytest.main()