from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from functools import wraps
from dbs.db_user import obtener_usuario_por_nombre, verificar_contrasena, registrar_usuario, usuario_existe

auth_bp = Blueprint('auth', __name__)

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = obtener_usuario_por_nombre(username)
        
        if user and verificar_contrasena(password, user[2]):
            session['user_id'] = user[0]
            session['user_role'] = user[3]
            session['user_username'] = user[1] 
            
            flash('Has iniciado sesión con éxito.')
            return redirect(url_for('index.index'))  # Redirigir a la página de inicio
        else:
            flash('Credenciales incorrectas.')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_requerido
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if not usuario_existe(username):
            registrar_usuario(username, password, role)
            flash('Registro exitoso.')
            return redirect(url_for('auth.login'))
        else:
            flash('El nombre de usuario ya está en uso.')
    return render_template('register.html')