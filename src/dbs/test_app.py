import unittest
import datetime
import requests
from colorama import init, Fore, Style

# Importar funciones de la base de datos (asegúrate de que estas funciones estén bien importadas)
from dbs.db_interface import cerrar, conectar
from dbs.db_money import eliminar_cuota, insertar_cuota, obtener_cuotas
from dbs.db_notification import eliminar_notificacion_db, insertar_notificacion, obtener_notificaciones
from dbs.db_voting import insertar_votacion, obtener_votaciones, registrar_voto

# Inicializamos colorama
init(autoreset=True)

class TestNotificaciones(unittest.TestCase):
    
    def setUp(self):
        """Crear una conexión temporal a la base de datos."""
        self.conn = conectar('Test.db')
        self.conn.execute("PRAGMA foreign_keys = ON")  # Activar claves foráneas para SQLite si es necesario
        self.fecha_actual = datetime.datetime.utcnow()

    def test_insertar_notificacion(self):
        """Prueba la inserción de una notificación."""
        resultado = insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual, path_db='Test.db')
        self.assertIsNone(resultado)  # Espera que no haya errores

    def test_obtener_notificaciones(self):
        """Prueba la obtención de notificaciones."""
        insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual, path_db='Test.db')
        notificaciones = obtener_notificaciones(path_db='Test.db')
        self.assertTrue(len(notificaciones) > 0)

    def test_eliminar_notificacion(self):
        """Prueba la eliminación de una notificación."""
        insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual, path_db='Test.db')
        notificaciones = obtener_notificaciones('Test.db')
        for notificacion in notificaciones:
            notificacion_id = notificacion if isinstance(notificacion, int) else notificacion[0]
            eliminar_notificacion_db(notificacion_id, 'Test.db')
        notificaciones = obtener_notificaciones('Test.db')
        self.assertEqual(len(notificaciones), 0)

    def tearDown(self):
        """Cerrar la conexión y limpiar la base de datos."""
        self.conn.rollback()
        cerrar(self.conn)


class TestMoney(unittest.TestCase):

    def setUp(self):
        self.conn = conectar('Test.db')
        self.conn.execute("PRAGMA foreign_keys = ON")
    
    def tearDown(self):
        self.conn.rollback()
        cerrar(self.conn)

    def test_insertar_cuota(self):
        resultado = insertar_cuota(1, "Cuota Prueba", 100.0, 'Test.db', 10.0)
        self.assertTrue(resultado)

    def test_obtener_cuotas(self):
        insertar_cuota(1, "Cuota Prueba", 100.0, 'Test.db')
        cuotas = obtener_cuotas('Test.db')
        self.assertTrue(len(cuotas) > 0)

    def test_eliminar_cuota(self):
        insertar_cuota(1, "Cuota Prueba", 100.0)
        cuotas = obtener_cuotas('Test.db')
        
        for cuota in cuotas:
            cuota_id = cuota if isinstance(cuota, int) else cuota[0]
            eliminar_cuota(cuota_id, 'Test.db')

        cuotas = obtener_cuotas('Test.db')
        self.assertEqual(len(cuotas), 0)


class TestVotaciones(unittest.TestCase):

    def setUp(self):
        self.conn = conectar('Test.db')
        self.conn.execute("PRAGMA foreign_keys = ON")

    def tearDown(self):
        self.conn.rollback()
        cerrar(self.conn)

    def test_insertar_votacion(self):
        resultado = insertar_votacion("Votación Prueba", "Opción 1, Opción 2", 'Test.db')
        self.assertIsNotNone(resultado)

    def test_obtener_votaciones(self):
        insertar_votacion("Votación Prueba", "Opción 1, Opción 2", 'Test.db')
        votaciones = obtener_votaciones('Test.db')
        self.assertTrue(len(votaciones) > 0)

    def test_registrar_voto(self):
        votacion_id = insertar_votacion("Votación Prueba", "Opción 1, Opción 2", 'Test.db')
        opciones = obtener_votaciones('Test.db')[votacion_id]['options']
        opcion_id = opciones[0]["id"]
        resultado = registrar_voto(opcion_id, 1, 'Test.db')
        self.assertTrue(resultado)


class TestEndpointAuth(unittest.TestCase):

    def test_login(self):
        # Datos de prueba para el login
        data = {
            "username": "admin",
            "password": "admin"
        }

        # Realiza la solicitud POST al endpoint /login
        response = requests.post(
            "http://127.0.0.1:5000/login",
            data=data,  # Enviar datos como formulario
            allow_redirects=False  # No seguir la redirección automáticamente
        )

        # Verifica el código de estado de redirección
        self.assertEqual(response.status_code, 302)  # Espera redirección 302

        # Verifica si la redirección es a la página de inicio
        self.assertEqual(response.headers["Location"], "/index")
        print(Fore.GREEN + "Credenciales correctas")

    def test_login_fail(self):
        # Intento de login con credenciales incorrectas
        data = {
            "username": "admin",
            "password": "wrongpassword"
        }

        response = requests.post(
            "http://127.0.0.1:5000/login",
            data=data,
            allow_redirects=False
        )

        # Verificar que el código de estado sea 200, ya que la página de login no redirige
        self.assertEqual(response.status_code, 200)

        print(Fore.RED +"Credenciales incorrectas")
