from flask import Flask, request
from config.settings import DefaultConfig
from controllers.auth import auth_bp
from controllers.votaciones import votaciones_bp
from controllers.notificaciones import notificaciones_bp
from controllers.dinero import dinero_bp
from controllers.usuarios import usuarios_bp
from controllers.index import index_bp

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

    @app.route('/greet')
    def greet():
        name = request.args.get('name', 'World')
        return f'Hola, {name}!'

    @app.route('/build')
    def build():
        return 'Construyendo el proyecto...'

    @app.route('/test')
    def test():
        return 'Ejecutando pruebas...'
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
