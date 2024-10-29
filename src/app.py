from flask import Flask
from controllers.auth import auth_bp
from controllers.votaciones import votaciones_bp
from controllers.notificaciones import notificaciones_bp
from controllers.dinero import dinero_bp
from controllers.usuarios import usuarios_bp
from controllers.index import index_bp

app = Flask(__name__)
app.secret_key = '123'  # Cambia esto por una clave secreta adecuada

# Registro de los Blueprints
app.register_blueprint(index_bp) 
app.register_blueprint(auth_bp)
app.register_blueprint(votaciones_bp)
app.register_blueprint(notificaciones_bp)
app.register_blueprint(dinero_bp)
app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(debug=True)
