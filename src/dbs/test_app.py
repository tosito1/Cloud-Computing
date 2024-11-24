import unittest
import datetime
import requests
from colorama import init, Fore, Style

# Importar funciones de la base de datos (asegúrate de que estas funciones estén bien importadas)
from dbs.db_interface import cerrar, conectar
from dbs.db_money import eliminar_cuota, insertar_cuota, obtener_cuotas
from dbs.db_notification import eliminar_notificacion_db, insertar_notificacion, obtener_notificaciones
from dbs.db_voting import insertar_votacion, obtener_votaciones, registrar_voto


