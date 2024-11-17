class DefaultConfig:
    """
    Configuración por defecto para la aplicación Flask.
    """
    DEBUG = True
    TESTING = False
    SECRET_KEY = "paquito-flores-key"  # Cambiar esta clave en producción
    JSON_SORT_KEYS = False