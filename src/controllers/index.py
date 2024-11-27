from flask import Blueprint, render_template
from controllers.auth import login_requerido

# Definir el Blueprint para la ruta de inicio
index_bp = Blueprint('index', __name__)

# Ruta principal, protegida por login_requerido
@index_bp.route('/')
@login_requerido
def home():
    return render_template('index.html')

# Ruta alternativa para la página de inicio (también protegida)
@index_bp.route('/index')
@login_requerido
def index():
    return render_template('index.html')
