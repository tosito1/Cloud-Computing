import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from db_interface import Base, create_database, obtener_notificaciones, crear_notificacion, eliminar_notificacion

@pytest.fixture(scope='module')
def test_database():
    # Crear la base de datos en memoria para las pruebas
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine  # Devuelve el motor para su uso en las pruebas

def test_crear_notificacion(test_database):
    # Crear una sesión conectada a la base de datos de prueba
    Session = sessionmaker(bind=test_database)
    session = Session()
    
    # Crear una notificación de prueba
    titulo = "Notificación de prueba"
    texto = "Este es el contenido de prueba de la notificación"
    user_id = 1  # Suponiendo que este ID de usuario de prueba existe
    fecha = date.today()
    
    # Llamada para crear la notificación
    crear_notificacion(session, titulo, texto, user_id, fecha)
    
    # Verificar que la notificación se ha creado correctamente
    notificaciones = obtener_notificaciones(session)
    assert any(n.titulo == titulo and n.texto == texto for n in notificaciones)

    session.close()

def test_eliminar_notificacion(test_database):
    # Crear una sesión conectada a la base de datos de prueba
    Session = sessionmaker(bind=test_database)
    session = Session()
    
    # Crear y agregar una notificación para eliminarla luego
    titulo = "Notificación a eliminar"
    texto = "Esta notificación será eliminada"
    user_id = 1
    fecha = date.today()
    crear_notificacion(session, titulo, texto, user_id, fecha)
    
    # Recuperar la notificación para obtener su ID
    notificaciones = obtener_notificaciones(session)
    notificacion_id = next((n.id for n in notificaciones if n.titulo == titulo), None)
    
    # Asegurarse de que la notificación se ha creado antes de eliminarla
    assert notificacion_id is not None, "No se pudo encontrar la notificación para eliminar"
    
    # Llamada para eliminar la notificación
    eliminar_notificacion(session, notificacion_id)
    
    # Verificar que la notificación ha sido eliminada
    notificaciones = obtener_notificaciones(session)
    assert all(n.id != notificacion_id for n in notificaciones)

    session.close()
