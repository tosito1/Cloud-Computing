import logging
from flask import Flask, request
from config.settings import DefaultConfig
from controllers.auth import auth_bp
from controllers.votaciones import votaciones_bp
from controllers.notificaciones import notificaciones_bp
from controllers.dinero import dinero_bp
from controllers.usuarios import usuarios_bp
from controllers.index import index_bp

# Configurar el logger
def configure_logging():
    """
    Configura el sistema de logging para guardar logs en un archivo y en la consola.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel de logging mínimo
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato
        handlers=[
            logging.FileHandler("app_logs.log"),  # Archivo para guardar los logs
            logging.StreamHandler()  # Mostrar también en consola
        ]
    )
    logging.getLogger("werkzeug").setLevel(logging.INFO)  # Reducir el nivel de logs de Flask por defecto


def create_app():
    """
    Crear y configurar una instancia de la aplicación Flask.
    """
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)

    # Registro de los Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(votaciones_bp)
    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(dinero_bp)
    app.register_blueprint(usuarios_bp)

    # Ejemplo de rutas básicas
    @app.route('/greet')
    def greet():
        name = request.args.get('name', 'World')
        app.logger.info(f"Greeting request for: {name}")
        return f'Hola, {name}!'

    @app.route('/build')
    def build():
        app.logger.info("Build endpoint was accessed.")
        return 'Construyendo el proyecto...'

    @app.route('/test')
    def test():
        app.logger.info("Test endpoint was accessed.")
        return 'Ejecutando pruebas...'

    return app


if __name__ == '__main__':
    configure_logging()  # Configurar el logging
    app = create_app()
    app.logger.info("Iniciando la aplicación Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host="127.0.0.1", port=5000, debug=True)  # Local
