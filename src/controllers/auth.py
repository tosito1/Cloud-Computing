from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
from services.auth_service import (
    verificar_contrasena
)
from services.user_service import obtener_usuario_username_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Decorador para verificar sesión activa
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('auth.login'))  # Redirige al formulario de login
        return f(*args, **kwargs)
    return decorated_function

# Endpoint: Inicio de sesión (API + HTML)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form['username']
            password = request.form['password']

        user = obtener_usuario_username_service(username)
        if user:
            # Convirtiendo el hash almacenado a bytes
            hashed_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
            # Verificando la contraseña
            if verificar_contrasena(password.encode('utf-8'), hashed_password):
                session['user_id'] = user['id']
                session['user_role'] = user['role']
                session['user_username'] = user['username']
                flash('Inicio de sesión exitoso.')
                if request.is_json:
                    return jsonify({"message": "Inicio de sesión exitoso."}), 200
                else:
                    return redirect(url_for('index.index'))
        error_message = "Credenciales incorrectas."
        if request.is_json:
            return jsonify({"error": error_message}), 401
        else:
            return render_template('login.html', error=error_message)
    return render_template('login.html') 

# Endpoint: Cierre de sesión
@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_requerido
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('user_username', None)
    flash('Has cerrado sesión exitosamente.')

    if request.is_json:
        return jsonify({"message": "Sesión cerrada exitosamente."}), 200
    else:
        return redirect(url_for('auth.login'))
