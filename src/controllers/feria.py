from flask import Blueprint, render_template
from controllers.auth import login_requerido

feria_bp = Blueprint('feria', __name__)

@feria_bp.route('/feria')
@login_requerido
def feria():
    return render_template('feria.html')  # Página de Feria
