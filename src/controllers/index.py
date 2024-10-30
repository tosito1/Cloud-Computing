from flask import Blueprint, render_template
from src.controllers.auth import login_requerido

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
@login_requerido
def home():
    return render_template('index.html') 

@index_bp.route('/index')
@login_requerido 
def index():
    return render_template('index.html') 