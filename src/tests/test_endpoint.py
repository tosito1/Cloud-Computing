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


class TestEndpointCuotas(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/dinero"
    admin_username = "admin"
    admin_password = "admin"
    session_cookies = None

    def setUp(self):
        # Autenticar al usuario 'admin' y almacenar las cookies de la sesión
        login_data = {
            "username": self.admin_username,
            "password": self.admin_password
        }
        response = requests.post(f"{self.base_url.replace('/dinero', '')}/auth/login", json=login_data)
        self.assertEqual(response.status_code, 200, "La autenticación de admin falló")
        self.session_cookies = response.cookies

    def test_get_cuotas(self):
        # Verificar si se obtienen las cuotas
        response = requests.get(f"{self.base_url}/", cookies=self.session_cookies, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        print(Fore.GREEN + "GET /dinero correcto")

    # def test_post_cuota(self):
    #     # Crear una nueva cuota
    #     data = {
    #         "amount": 50.0,
    #         "quota_name": "Cuota de prueba",
    #         "user_id": 1
    #     }
    #     response = requests.post(f"{self.base_url}/", cookies=self.session_cookies, json=data)
    #     self.assertEqual(response.status_code, 201)
    #     print(Fore.GREEN + "POST /dinero/ correcto")

    def test_delete_cuota(self):
        # Crear una cuota de prueba para eliminar
        data = {"amount": 100, "quota_name": "Cuota a eliminar","user_id": 1}
        create_response = requests.post(f"{self.base_url}/", cookies=self.session_cookies, json=data)
        self.assertEqual(create_response.status_code, 201, "Error al crear una cuota para eliminar")
        print(Fore.GREEN + "POST /dinero/ correcto")

        # Obtener las cuotas para encontrar la creada
        # get_response = requests.get(f"{self.base_url}/", cookies=self.session_cookies, headers={"Accept": "application/json"})
        # self.assertEqual(get_response.status_code, 200, "Error al obtener las cuotas")

        get_response = requests.get(
            f"{self.base_url}",
            cookies=self.session_cookies,
            headers={"Accept": "application/json"}
        )
        self.assertEqual(get_response.status_code, 200)
        cuotas = get_response.json()
        self.assertTrue(len(cuotas) > 0, "No hay cuotas disponibles para eliminar")

        # # Obtener el ID de la última cuota (ajustar según el formato de respuesta)
        cuota_id = cuotas[-1][0]  # Suponiendo que el ID es el primer elemento de cada lista
        self.assertIsInstance(cuota_id, int, "El ID de la cuota no es un entero")

        # # Eliminar la cuota
        delete_response = requests.post(f"{self.base_url}/{cuota_id}/eliminar", cookies=self.session_cookies)
        self.assertEqual(delete_response.status_code, 200, "Error al eliminar la cuota")
        print(Fore.GREEN + "DELETE /dinero correcto")


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


class TestEndpointNotificaciones(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"
    admin_username = "admin"
    admin_password = "admin"
    session_cookies = None

    def setUp(self):
        # Autenticar al usuario 'admin' y almacenar las cookies de la sesión
        login_data = {
            "username": self.admin_username,
            "password": self.admin_password
        }
        response = requests.post(f"{self.base_url}/auth/login", json=login_data)
        self.assertEqual(response.status_code, 200, "La autenticación de admin falló")
        self.session_cookies = response.cookies

    def test_get_notificaciones(self):
        # Verificar si se obtienen las notificaciones
        response = requests.get(f"{self.base_url}/notificaciones", cookies=self.session_cookies, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        notificaciones = response.json()
        self.assertTrue(isinstance(notificaciones, list))
        print(Fore.GREEN + "GET /notificaciones correcto")

    def test_post_notificacion(self):
        # Crear una nueva notificación
        data = {"titulo": "Nueva Notificación", "texto": "Texto de prueba"}
        response = requests.post(f"{self.base_url}/notificaciones", cookies=self.session_cookies, data=data)
        self.assertEqual(response.status_code, 200)
        print(Fore.GREEN + "POST /notificaciones correcto")

    def test_delete_notificacion(self):
        # Obtener la lista de notificaciones
        get_response = requests.get(
            f"{self.base_url}/notificaciones",
            cookies=self.session_cookies,
            headers={"Accept": "application/json"}
        )
        self.assertEqual(get_response.status_code, 200)

        # Imprimir la respuesta para depuración
        notificaciones = get_response.json()
        #print("Respuesta del servidor:", notificaciones)

        # Asegurarse de que la respuesta sea una lista válida
        self.assertTrue(isinstance(notificaciones, list), "La respuesta no es una lista")
        self.assertGreater(len(notificaciones), 0, "No hay notificaciones disponibles para eliminar")

        # Obtener el ID de la última notificación (ajustando para listas)
        notificacion_id = notificaciones[-1][0]  # Suponiendo que el ID es el primer elemento de la lista interna
        self.assertIsInstance(notificacion_id, int, "El ID de la notificación no es un entero")

        # Eliminar la notificación
        delete_response = requests.post(
            f"{self.base_url}/notificaciones/{notificacion_id}/eliminar",
            cookies=self.session_cookies
        )
        self.assertEqual(delete_response.status_code, 200)

        print(Fore.GREEN + "DELETE /notificaciones correcto")
