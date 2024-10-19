import datetime
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.models import db, User, Notificacion, Votacion, Opcion  # Importa todo desde models.py


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socios.db'
db.init_app(app)  # Usa la instancia de db desde models.py
login_manager = LoginManager()
login_manager.init_app(app)

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas de la aplicación
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # No uses esto en producción, utiliza hashing
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Inicio de sesión fallido. Verifica tus credenciales.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['role']  # Obtener el rol del formulario
        new_user = User(username=username, password=password, role=rol)  # Asignar el rol aquí
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/notificaciones', methods=['GET', 'POST', 'DELETE'])
@login_required
def notificaciones():
    if request.method == 'POST':
        if current_user.role == 'presidente':  # Asegurarse de que solo los presidentes puedan añadir notificaciones
            titulo = request.form['titulo']
            mensaje = request.form['mensaje']
            notificacion = Notificacion(
                titulo=titulo,
                mensaje=mensaje,
                presidente_id=current_user.id,
                fecha=datetime.datetime.now()
            )
            db.session.add(notificacion)
            db.session.commit()
            flash('Notificación añadida con éxito.', 'success')
            return redirect(url_for('notificaciones'))
    elif request.method == 'DELETE':
        if current_user.role == 'presidente':
            notificacion_id = request.form['id']
            notificacion = Notificacion.query.get(notificacion_id)
            db.session.delete(notificacion)
            db.session.commit()
            flash('Notificación eliminada con éxito.', 'success')
            return redirect(url_for('notificaciones'))
    
    # Obtener todas las notificaciones para mostrarlas en la página
    notificaciones = Notificacion.query.all()
    return render_template('notificaciones.html', notificaciones=notificaciones)


@app.route('/votaciones', methods=['GET', 'POST'])
@login_required
def votaciones():
    if request.method == 'POST':
        if current_user.role == 'presidente':
            # Comprobación de si se desea eliminar una votación
            if 'accion' in request.form and request.form['accion'] == 'eliminar':
                votacion_id = request.form['id']
                votacion = Votacion.query.get(votacion_id)
                if votacion:
                    db.session.delete(votacion)
                    db.session.commit()
                    flash('Votación eliminada con éxito.', 'success')
                else:
                    flash('Votación no encontrada.', 'danger')
                return redirect(url_for('votaciones'))

            # Creación de nueva votación
            titulo = request.form['titulo']
            opciones_input = request.form['opciones']
            opciones = [opcion.strip() for opcion in opciones_input.split(',')]

            votacion = Votacion(titulo=titulo, fecha=datetime.datetime.now())
            db.session.add(votacion)
            db.session.commit()

            for opcion in opciones:
                nueva_opcion = Opcion(descripcion=opcion, votacion_id=votacion.id)
                db.session.add(nueva_opcion)
            
            db.session.commit()
            flash('Votación añadida con éxito.', 'success')
            return redirect(url_for('votaciones'))

    votaciones = Votacion.query.all()
    return render_template('votaciones.html', votaciones=votaciones, current_user=current_user)


@app.route('/dinero', methods=['GET'])
@login_required
def dinero():
    return render_template('dinero.html')

@app.route('/san_juan')
@login_required
def san_juan():
    return render_template('san_juan.html')

@app.route('/feria')
@login_required
def feria():
    return render_template('feria.html')

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea la base de datos y las tablas
    app.run(debug=True)
