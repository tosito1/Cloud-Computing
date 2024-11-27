

from flask import Flask

from config.settings import SettingConfig

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object(SettingConfig)

# Registrar rutas y otros módulos
from app import routes  # Importar las rutas de la aplicación



# Paquito Flores/
# ├── src/
# │   ├── __init__.py       # Inicialización del microservicio
# │   ├── controllers/          # Controladores para cada servicio
# │   │   ├── __init__.py
# │   │   ├── notificationes.py  # Controlador para notificaciones
# │   │   ├── dinero.py         # Controlador para cuotas y multas
# │   │   ├── votaciones.py          # Controlador para votaciones
# │   │   ├── index.py          # Controlador para index
# │   │   ├── usuarios.py          # Controlador para registrar usuarios
# │   │   └── auth.py           # Controlador para autenticación
# │   ├── services/         # Lógica de negocio y funcionalidades principales
# │   │   ├── __init__.py
# │   │   ├── notifications_service.py  # Servicio para manejar notificaciones
# │   │   ├── voting_service.py         # Servicio para manejar votaciones
# │   │   ├── quotas_service.py         # Servicio para manejar cuotas
# │   ├── tests/            # Pruebas unitarias para las rutas y lógica de negocio
# │   │   ├── __init__.py
# │   │   ├── test_notifications.py    # Pruebas para el servicio de notificaciones
# │   │   ├── test_routes.py           # Pruebas para las rutas
# │   ├── config/           # Configuración del microservicio
# │   │   ├── __init__.py
# │   │   ├── settings.py              # Variables y ajustes generales
# │   ├── utils/            # Funciones reutilizables como logs, validaciones, etc.
# │   │   ├── __init__.py
# │   │   ├── logger.py               # Configuración y manejo de logs
# │   └── templates/
# │   │   ├── index.html
# │   │   ├── notificaciones.html
# │   │   ├── usuarios.html
# │   │   ├── login.html
# │   │   └── register.html
# ├── requirements.txt      # Dependencias del proyecto
# ├── Makefile              # Comandos automatizados
# ├── README.md             # Documentación del proyecto