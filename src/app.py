from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from dbs.db_user import (
    insertar_usuario, obtener_usuario_por_id, obtener_usuario_por_nombre, actualizar_usuario, eliminar_usuario, registrar_usuario, usuario_existe, verificar_contrasena
)
from dbs.db_notification import (
    insertar_notificacion, obtener_notificaciones, actualizar_notificacion, eliminar_notificacion
)
from dbs.db_voting import (
    insertar_votacion, insertar_opcion, obtener_votaciones, actualizar_votacion, eliminar_votacion
)
from dbs.db_money import (
    insertar_cuota, insertar_multa, obtener_cuotas, obtener_multas, actualizar_cuota, eliminar_cuota
)

app = Flask(__name__)
app.secret_key = '123'  # Cambia esto por una clave secreta adecuada

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta de inicio
@app.route('/')
@login_requerido
def home():
    return render_template('index.html')  # Página de inicio

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Obtiene el usuario de la base de datos
        user = obtener_usuario_por_nombre(username)
        
        # Verifica si el usuario existe y la contraseña es correcta
        if user and verificar_contrasena(password, user[2]):  # Asumiendo que el índice 2 contiene la contraseña hasheada
            session['user_id'] = user[0]  # Guarda el ID del usuario en la sesión (asumiendo que el ID está en el índice 0)
            flash('Has iniciado sesión con éxito.')
            return redirect(url_for('index'))  # Redirige a la página de inicio
        else:
            flash('Credenciales incorrectas.')

    return render_template('login.html')  # Renderiza el formulario de inicio de sesión
    
@app.route('/logout')
@login_requerido
def logout():
    session.pop('user_id', None)  # Elimina el ID del usuario de la sesión
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

# Ruta de índice
@app.route('/index')
@login_requerido
def index():
    return render_template('index.html')  # Página de índice

# Rutas de Votaciones
@app.route('/votaciones', methods=['GET', 'POST'])
@login_requerido
def votaciones():
    if request.method == 'POST':
        # Crear nueva votación
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        insertar_votacion(titulo, descripcion)  # Función para insertar votación
        flash('Votación creada con éxito')
        return redirect(url_for('votaciones'))

    votaciones = obtener_votaciones()  # Obtener todas las votaciones
    return render_template('votaciones.html', votaciones=votaciones)

@app.route('/votaciones/<int:votacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_votacion(votacion_id):
    eliminar_votacion(votacion_id)  # Eliminar votación
    flash('Votación eliminada con éxito')
    return redirect(url_for('votaciones'))

@app.route('/votaciones/<int:votacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_votacion(votacion_id):
    votacion = obtener_votaciones(votacion_id)  # Obtén la votación a editar
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        actualizar_votacion(votacion_id, titulo, descripcion)  # Función para actualizar votación
        flash('Votación actualizada con éxito')
        return redirect(url_for('votaciones'))
    return render_template('editar_votacion.html', votacion=votacion)

# Rutas de Dinero
@app.route('/dinero', methods=['GET', 'POST'])
@login_requerido
def dinero():
    if request.method == 'POST':
        # Crear nueva cuota
        monto = request.form['monto']
        insertar_cuota(monto)  # Función para insertar cuota
        flash('Cuota creada con éxito')
        return redirect(url_for('dinero'))

    cuotas = obtener_cuotas()  # Obtener todas las cuotas
    multas = obtener_multas()  # Obtener todas las multas
    return render_template('dinero.html', cuotas=cuotas, multas=multas)

@app.route('/dinero/cuota/<int:cuota_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_cuota(cuota_id):
    cuota = obtener_cuota_por_id(cuota_id)  # Debes definir esta función en tu módulo de dinero
    if request.method == 'POST':
        monto = request.form['monto']
        actualizar_cuota(cuota_id, monto)  # Función para actualizar cuota
        flash('Cuota actualizada con éxito')
        return redirect(url_for('dinero'))
    return render_template('editar_cuota.html', cuota=cuota)

@app.route('/dinero/multa', methods=['POST'])
@login_requerido
def agregar_multa():
    # Crear nueva multa
    monto = request.form['monto']
    insertar_multa(monto)  # Función para insertar multa
    flash('Multa creada con éxito')
    return redirect(url_for('dinero'))

# Rutas de Notificaciones
@app.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    if request.method == 'POST':
        # Crear nueva notificación
        titulo = request.form['titulo']
        texto = request.form['texto']
        insertar_notificacion(titulo, texto)  # Función para insertar notificación
        flash('Notificación creada con éxito')
        return redirect(url_for('notificaciones'))

    notificaciones = obtener_notificaciones()  # Obtener todas las notificaciones
    return render_template('notificaciones.html', notificaciones=notificaciones)

@app.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    eliminar_notificacion(notificacion_id)  # Eliminar notificación
    flash('Notificación eliminada con éxito')
    return redirect(url_for('notificaciones'))

@app.route('/notificaciones/<int:notificacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_notificacion(notificacion_id):
    notificacion = obtener_notificacion_por_id(notificacion_id)  # Debes definir esta función
    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        actualizar_notificacion(notificacion_id, titulo, texto)  # Función para actualizar notificación
        flash('Notificación actualizada con éxito')
        return redirect(url_for('notificaciones'))
    return render_template('editar_notificacion.html', notificacion=notificacion)

# Rutas de Usuarios
@app.route('/usuarios', methods=['GET', 'POST'])
@login_requerido
def usuarios():
    if request.method == 'POST':
        # Crear nuevo usuario
        username = request.form['username']
        password = request.form['password']
        insertar_usuario(username, password)  # Función para insertar usuario
        flash('Usuario creado con éxito')
        return redirect(url_for('usuarios'))

    usuarios = obtener_usuarios()  # Obtener todos los usuarios
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/<int:user_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_usuario(user_id):
    eliminar_usuario(user_id)  # Eliminar usuario
    flash('Usuario eliminado con éxito')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_usuario(user_id):
    usuario = obtener_usuario_por_id(user_id)  # Obtén el usuario a editar
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        actualizar_usuario(user_id, username, password)  # Función para actualizar usuario
        flash('Usuario actualizado con éxito')
        return redirect(url_for('usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)


# Rutas de Feria
@app.route('/feria')
@login_requerido
def feria():
    return render_template('feria.html')  # Página de feria

# Ruta de san juan
@app.route('/san_juan')
@login_requerido
def san_juan():
    return render_template('san_juan.html')  # Página de san juan

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Asegúrate de encriptar la contraseña antes de guardarla
        role = request.form['role']

        # Verifica si el nombre de usuario ya existe
        if not usuario_existe(username):  # Implementa esta función para verificar en la base de datos
            registrar_usuario(username, password, role)  # Asegúrate de que esta función acepte el rol
            flash('Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        else:
            flash('El nombre de usuario ya está en uso.')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)