from flask import Flask, request
from src.controllers.auth import auth_bp
from src.controllers.votaciones import votaciones_bp
from src.controllers.notificaciones import notificaciones_bp
from src.controllers.dinero import dinero_bp
from src.controllers.usuarios import usuarios_bp
from src.controllers.index import index_bp

app = Flask(__name__)
app.secret_key = '123'  # Cambia esto por una clave secreta adecuada

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

if __name__ == '__main__':
    app.run(debug=True)
