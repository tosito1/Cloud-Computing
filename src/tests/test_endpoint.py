import unittest
from colorama import Fore
import requests

class TestEndpointAuth(unittest.TestCase):

    base_url = "http://127.0.0.1:5000"

    def test_login_success(self):
        data = {
            "username": "admin",
            "password": "admin"
        }
        response = requests.post(f"{self.base_url}/auth/login", json=data)
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        data = {
            "username": "admin",
            "password": "wrongpassword"
        }

        response = requests.post(f"{self.base_url}/auth/login", json=data)
        self.assertEqual(response.status_code, 401)  # Error de autorización


class TestEndpointUsuarios(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def test_get_usuarios(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        print(Fore.GREEN + "GET /usuarios correcto")

    def test_post_usuario(self):
        nuevo_usuario = "nuevo_usuario"
        data = {"username": nuevo_usuario, "password": "password123", "role": "administrador"}

        # Verificar si el usuario ya existe y eliminarlo
        # response_check = requests.get(f"{self.base_url}/usuarios/{nuevo_usuario}")
        # if response_check.status_code == 200:
        #     requests.delete(f"{self.base_url}/usuarios/{nuevo_usuario}")

        # Crear el usuario
        response = requests.post(f"{self.base_url}/usuarios", json=data)
        self.assertEqual(response.status_code, 201)
        print(Fore.GREEN + "POST /usuarios correcto")

        # Eliminar el usuario creado
        delete_response = requests.delete(f"{self.base_url}/usuarios/{nuevo_usuario}", allow_redirects=True)
        self.assertEqual(delete_response.status_code, 200)
        print(Fore.GREEN + "DELETE /usuarios correcto")


# class TestEndpointDinero(unittest.TestCase):

#     def setUp(self):
#         self.base_url = "http://127.0.0.1:5000/dinero"

#     def test_get_cuotas(self):
#         # Realiza una solicitud GET al endpoint de cuotas
#         response = requests.get(self.base_url)
        
#         # Verificar que el código de estado sea 200
#         self.assertEqual(response.status_code, 200)

#         # Verificar que el contenido sea JSON válido (si aplica)
#         self.assertTrue(response.headers["Content-Type"].startswith("application/json"))
#         print(Fore.GREEN + "GET /dinero correcto")

#     def test_post_cuotas(self):
#         # Datos de prueba para crear una nueva cuota
#         data = {
#             "monto": 150.0,
#             "descripcion": "Test cuota"
#         }

#         response = requests.post(self.base_url, json=data)

#         # Verificar que el código de estado sea 201 (creado)
#         self.assertEqual(response.status_code, 201)

#         # Verificar respuesta JSON
#         self.assertIn("message", response.json())
#         print(Fore.GREEN + "POST /dinero correcto")

#     def test_post_cuotas_invalidas(self):
#         # Datos inválidos
#         data = {
#             "monto": -50.0,  # Monto negativo no válido
#             "descripcion": ""
#         }

#         response = requests.post(self.base_url, json=data)

#         # Verificar que el código de estado sea 400 (solicitud incorrecta)
#         self.assertEqual(response.status_code, 400)

#         # Verificar respuesta JSON
#         self.assertIn("error", response.json())
#         print(Fore.RED + "POST /dinero inválido detectado correctamente")


# class TestEndpointVotaciones(unittest.TestCase):

#     def setUp(self):
#         self.base_url = "http://127.0.0.1:5000/votaciones"

#     def test_get_votaciones(self):
#         response = requests.get(self.base_url)

#         # Verificar que el código de estado sea 200
#         self.assertEqual(response.status_code, 200)

#         # Verificar que el contenido sea JSON válido (si aplica)
#         self.assertTrue(response.headers["Content-Type"].startswith("application/json"))
#         print(Fore.GREEN + "GET /votaciones correcto")

#     def test_post_votacion(self):
#         data = {
#             "titulo": "Test votación",
#             "opciones": "Opción 1, Opción 2"
#         }

#         response = requests.post(self.base_url, json=data)

#         # Verificar que el código de estado sea 201 (creado)
#         self.assertEqual(response.status_code, 201)

#         self.assertIn("message", response.json())
#         print(Fore.GREEN + "POST /votaciones correcto")

#     def test_post_votacion_invalida(self):
#         data = {
#             "titulo": "",  # Título vacío no válido
#             "opciones": ""
#         }

#         response = requests.post(self.base_url, json=data)

#         # Verificar que el código de estado sea 400 (solicitud incorrecta)
#         self.assertEqual(response.status_code, 400)

#         self.assertIn("error", response.json())
#         print(Fore.RED + "POST /votaciones inválido detectado correctamente")


# class TestEndpointNotificaciones(unittest.TestCase):

#     def setUp(self):
#         self.base_url = "http://127.0.0.1:5000/notificaciones"

#     def test_get_notificaciones(self):
#         response = requests.get(self.base_url)

#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.headers["Content-Type"].startswith("application/json"))
#         print(Fore.GREEN + "GET /notificaciones correcto")

#     def test_post_notificacion(self):
#         data = {
#             "titulo": "Título prueba",
#             "mensaje": "Mensaje de prueba",
#             "usuario_id": 1
#         }

#         response = requests.post(self.base_url, json=data)

#         self.assertEqual(response.status_code, 201)
#         self.assertIn("message", response.json())
#         print(Fore.GREEN + "POST /notificaciones correcto")

#     def test_post_notificacion_invalida(self):
#         data = {
#             "titulo": "",
#             "mensaje": "",
#             "usuario_id": None  # Usuario no válido
#         }

#         response = requests.post(self.base_url, json=data)

#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.json())
#         print(Fore.RED + "POST /notificaciones inválido detectado correctamente")
