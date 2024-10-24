from flask import Blueprint, render_template
from controllers.auth import login_requerido

san_juan_bp = Blueprint('san_juan', __name__)

@san_juan_bp.route('/san_juan')
@login_requerido
def san_juan():
    return render_template('san_juan.html')  # Página de San Juan
