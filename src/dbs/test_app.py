import unittest
import datetime

from dbs.db_interface import cerrar, conectar
from dbs.db_money import eliminar_cuota, insertar_cuota, obtener_cuotas
from dbs.db_notification import eliminar_notificacion_db, insertar_notificacion, obtener_notificaciones
from dbs.db_voting import insertar_votacion, obtener_votaciones, registrar_voto

class TestNotificaciones(unittest.TestCase):
    
    def setUp(self):
        """Crear una conexión temporal a la base de datos."""
        self.conn = conectar('Test.db')
        self.conn.execute("PRAGMA foreign_keys = ON")  # Activar claves foráneas para SQLite si es necesario
        self.fecha_actual = datetime.datetime.utcnow()

    def test_insertar_notificacion(self):
        """Prueba la inserción de una notificación."""
        resultado = insertar_notificacion("Título Prueba", "Mensaje Prueba", 1,self.fecha_actual, path_db = 'Test.db')
        self.assertIsNone(resultado)  # Espera que no haya errores

    def test_obtener_notificaciones(self):
        """Prueba la obtención de notificaciones."""
        insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual, path_db = 'Test.db')
        notificaciones = obtener_notificaciones(path_db = 'Test.db')
        self.assertTrue(len(notificaciones) > 0)

    # def test_actualizar_notificacion(self):
    #     """Prueba la actualización de una notificación."""
    #     insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual)
    #     notificaciones = obtener_notificaciones()
    #     notificacion_id = notificaciones[0][0]
    #     actualizar_notificacion(notificacion_id, "Título Actualizado", "Mensaje Actualizado")
    #     notificaciones = obtener_notificaciones()
    #     self.assertEqual(notificaciones[0][1], "Título Actualizado")

    def test_eliminar_notificacion(self):
        """Prueba la eliminación de una notificación."""
        insertar_notificacion("Título Prueba", "Mensaje Prueba", 1, self.fecha_actual, path_db = 'Test.db')
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

    # def test_actualizar_cuota(self):
    #     insertar_cuota(1, "Cuota Prueba", 100.0)
    #     cuotas = obtener_cuotas()
    #     cuota_id = cuotas[0][0]
    #     actualizar_cuota(cuota_id, 150.0, datetime.datetime.utcnow())
    #     cuotas = obtener_cuotas()
    #     self.assertEqual(cuotas[0][2], 150.0)

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
        insertar_votacion("Votación Prueba", "Opción 1, Opción 2",'Test.db')
        votaciones = obtener_votaciones('Test.db')
        self.assertTrue(len(votaciones) > 0)

    # def test_actualizar_votacion(self):
    #     votacion_id = insertar_votacion("Votación Prueba", "Opción 1, Opción 2")
    #     actualizar_votacion(votacion_id, "Votación Actualizada", "Opción 1, Opción 2")
    #     votaciones = obtener_votaciones()
    #     self.assertEqual(votaciones[votacion_id]["title"], "Votación Actualizada")

    # def test_eliminar_votacion(self):
    #     votacion_id = insertar_votacion("Votación Prueba", "Opción 1, Opción 2", 'Test.db')
    #     eliminar_votacion_db(votacion_id)
    #     votaciones = obtener_votaciones()
    #     self.assertNotIn(votacion_id, votaciones)

    def test_registrar_voto(self):
        votacion_id = insertar_votacion("Votación Prueba", "Opción 1, Opción 2",'Test.db')
        opciones = obtener_votaciones('Test.db')[votacion_id]['options']
        opcion_id = opciones[0]["id"]
        resultado = registrar_voto(opcion_id, 1, 'Test.db')
        self.assertTrue(resultado)
