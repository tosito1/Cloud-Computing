import logging
from fluent import handler
from flask import Flask, render_template, request, redirect, url_for
from extensions import db 
from models import Fine, User, Notification, Quota, Vote, Voting, Option
from sqlalchemy.exc import SQLAlchemyError
import datetime
from werkzeug.security import generate_password_hash

from flask import render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
import bcrypt

# Configuración para enviar logs a Fluentd
fluent_handler = handler.FluentHandler('app.logs', host='logs', port=24224)
formatter = handler.FluentRecordFormatter({'message': '%(asctime)s [%(levelname)s] %(message)s'})
fluent_handler.setFormatter(formatter)

# Configuración del logger
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(fluent_handler)

# Ejemplo de log
logger.info("Aplicación iniciada correctamente.")

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app_db_ncgb_user:jrhbHnKdMYKCclubX0RPPJUF5b9pON4E@dpg-cu9ln4jqf0us73c1j340-a/app_db_ncgb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)



####################        ENDPOINT        ######################

####################        LOGIN           ######################

# Ruta para mostrar el formulario
# Decorador para verificar sesión activa
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            app.logger.warning('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('login'))  # Redirige al formulario de login
        return f(*args, **kwargs)
    return decorated_function

# Endpoint: Inicio de sesión (API + HTML)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form['username']
            password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            # Convirtiendo el hash almacenado a bytes
            # hashed_password = user.password_hash.encode('utf-8') if isinstance(user.password_hash, str) else user.password_hash
            # Verificando la contraseña
            # if verificar_contrasena(password.encode('utf-8'), hashed_password):
            if user.password_hash==password:
                session['user_id'] = user.id
                session['user_role'] = user.role
                session['user_username'] = user.username
                app.logger.info(f"'{user.id}'Inicio de sesión exitoso.")
                if request.is_json:
                    return jsonify({"message": "Inicio de sesión exitoso."}), 200
                else:
                    return redirect(url_for('index'))
        error_message = "Credenciales incorrectas."
        if request.is_json:
            return jsonify({"error": error_message}), 401
        else:
            return render_template('login.html', error=error_message)
    return render_template('login.html') 

# Endpoint: Cierre de sesión
@app.route('/logout', methods=['GET', 'POST'])
@login_requerido
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('user_username', None)
    app.logger.info('Has cerrado sesión exitosamente.')

    if request.is_json:
        return jsonify({"message": "Sesión cerrada exitosamente."}), 200
    else:
        return redirect(url_for('login'))

def hash_password(password: str) -> str:
    """Hashea la contraseña usando bcrypt y retorna el hash como una cadena."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Convertimos a cadena


def verificar_contrasena(password: bytes, hashed_password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con la contraseña hasheada."""
    # Asegúrate de que el hash es un byte string
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

##################      INDEX       ####################

@app.route('/')
@login_requerido
def home():
    return render_template('index.html')

# Ruta alternativa para la página de inicio (también protegida)
@app.route('/index')
@login_requerido
def index():
    return render_template('index.html')

##################      Notificaciones      ##################
@app.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    user_id = session.get('user_id')
    usuario_actual = User.query.get(user_id)  # Obtener los datos del usuario actual

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')

        if not titulo or not texto:
            app.logger.warning('Título y texto son obligatorios', 'error')
            return redirect(url_for('notificaciones'))

        try:
            # Crear nueva notificación
            nueva_notificacion = Notification(
                title=titulo,
                text=texto,
                president_id=user_id,  # Asegurarse de usar president_id aquí
                date=datetime.datetime.now()
            )
            db.session.add(nueva_notificacion)
            db.session.commit()
            app.logger.info('Notificación creada con éxito')
            return redirect(url_for('notificaciones'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al crear la notificación: {str(e)}"
            app.logger.warning(error_msg)
            return redirect(url_for('notificaciones'))

    # Obtener todas las notificaciones, sin importar el usuario
    notificaciones = Notification.query.all()

    # Si la solicitud espera JSON
    if request.headers.get("Accept") == "application/json":
        notificaciones_serializadas = [
            {"id": n.id, "title": n.title, "content": n.text, "created_at": n.date.isoformat()}
            for n in notificaciones
        ]
        return jsonify(notificaciones_serializadas)

    # Renderizar la plantilla HTML
    return render_template('notificaciones.html', notificaciones=notificaciones, current_user=usuario_actual)

@app.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    try:
        notificacion = Notification.query.get(notificacion_id)

        if not notificacion or notificacion.president_id != session.get('user_id'):
            app.logger.warning('Notificación no encontrada o acceso denegado')
            if request.headers.get("Accept") == "application/json":
                return jsonify({"status": "error", "message": "Notificación no encontrada o acceso denegado"}), 404
            return redirect(url_for('notificaciones'))

        db.session.delete(notificacion)
        db.session.commit()
        app.logger.info('Notificación eliminada con éxito')

        # Respuesta en JSON para los tests
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "success", "message": "Notificación eliminada con éxito"}), 200

        # Redirigir a la página de notificaciones
        return redirect(url_for('notificaciones'))

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = f"Error al eliminar la notificación: {str(e)}"
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "error", "message": error_msg}), 500

        app.logger.warning(error_msg)
        return redirect(url_for('notificaciones'))

@app.route('/notificaciones/<int:notificacion_id>/editar', methods=['GET', 'POST'])
#@login_requerido
def editar_notificacion(notificacion_id):
    notificacion = Notification.query.get(notificacion_id)

    if not notificacion or notificacion.user_id != session.get('user_id'):
        app.logger.warning('Notificación no encontrada o acceso denegado')
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "error", "message": "Notificación no encontrada o acceso denegado"}), 404
        return redirect(url_for('notificaciones'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')

        if not titulo or not texto:
            app.logger.warning('Título y texto son obligatorios')
            return redirect(url_for('notificaciones.editar_notificacion', notificacion_id=notificacion_id))

        try:
            # Actualizar la notificación
            notificacion.title = titulo
            notificacion.content = texto
            db.session.commit()
            app.logger.info('Notificación actualizada con éxito')
            return redirect(url_for('notificaciones'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al actualizar la notificación: {str(e)}"
            app.logger.warning(error_msg)
            return redirect(url_for('notificaciones.editar_notificacion', notificacion_id=notificacion_id))

    if request.headers.get("Accept") == "application/json":
        return jsonify({
            "id": notificacion.id,
            "title": notificacion.title,
            "content": notificacion.content,
            "created_at": notificacion.created_at.isoformat()
        })

    return render_template('editar_notificacion.html', notificacion=notificacion)

####################        Cuotas      ###############################
@app.route('/dinero', methods=['GET', 'POST'])
@login_requerido
def dinero():
    if request.method == 'POST':
        try:
            # Verifica si la solicitud es JSON o un formulario
            if request.is_json:
                data = request.get_json()
                dinero = data.get('amount')
                nombre_cuota = data.get('quota_name')
                username = data.get('user_id')
                multa_cantidad = data.get('multa_amount')
            else:
                dinero = request.form['amount']
                nombre_cuota = request.form['quota_name']
                username = request.form['user_id']
                multa_cantidad = request.form.get('multa_amount')
            # Validar la cantidad de dinero
            dinero = float(dinero)
            
            user = User.query.filter_by(username=username).first()
            if not user:
                raise ValueError("El usuario no existe")

            # Crear multa si se proporciona una cantidad
            fine_id = None
            if multa_cantidad:
                multa_cantidad = float(multa_cantidad)
                if multa_cantidad <= 0:
                    raise ValueError("La multa debe ser un valor positivo")
                
                nueva_multa = Fine(
                    user_id=user.id,
                    amount=multa_cantidad
                )
                db.session.add(nueva_multa)
                db.session.flush()  # Para obtener el ID de la multa
                fine_id = nueva_multa.id

            # Determinar el estado basado en la multa
            status = "multa" if fine_id else "pagado"

            # Crear nueva cuota
            nueva_cuota = Quota(
                user_id=user.id,
                name=nombre_cuota,
                amount=dinero,
                status=status,
                fine_id=fine_id
            )
            db.session.add(nueva_cuota)
            db.session.commit()

            app.logger.info('Cuota creada con éxito')
            if request.is_json:
                return jsonify({"message": "Cuota creada con éxito"}), 201
            else:
                return redirect(url_for('dinero'))

        except ValueError as e:
            flash(str(e), 'error')
            if request.is_json:
                return jsonify({"error": str(e)}), 400
            return redirect(url_for('dinero'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = "Error al crear la cuota: " + str(e)
            app.logger.warning(error_msg)
            if request.is_json:
                return jsonify({"error": error_msg}), 500
            return redirect(url_for('dinero'))
    # Obtener cuotas y usuarios
    usuarios = User.query.all()
    cuotas = Quota.query.all()
    multas = Fine.query.all()
    if request.headers.get("Accept") == "application/json":
        cuotas_serializadas = [{"id": c.id, "user_id": c.user_id, "quota_name": c.quota_name, "amount": c.amount} for c in cuotas]
        return jsonify(cuotas_serializadas), 200
    else:
        return render_template('dinero.html', cuotas=cuotas, multas=multas, usuarios=usuarios)

@app.route('/dinero/<int:cuota_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_cuota_route(cuota_id):
    try:
        cuota = Quota.query.get(cuota_id)
        if not cuota:
            app.logger.warning('Cuota no encontrada')
            if request.is_json:
                return jsonify({"error": "Cuota no encontrada"}), 404
            return redirect(url_for('dinero'))

        db.session.delete(cuota)
        db.session.commit()
        app.logger.info('Cuota eliminada con éxito')

        if request.is_json:
            return jsonify({"message": "Cuota eliminada con éxito"}), 200
        else:
            return redirect(url_for('dinero'))
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = "Error al eliminar la cuota: " + str(e)
        app.logger.warning(error_msg)
        if request.is_json:
            return jsonify({"error": error_msg}), 500
        return redirect(url_for('dinero'))

@app.route('/dinero/<int:cuota_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_cuota(cuota_id):
    cuota = Quota.query.get(cuota_id)
    if not cuota:
        app.logger.warning('Cuota no encontrada')
        if request.is_json:
            return jsonify({"error": "Cuota no encontrada"}), 404
        return redirect(url_for('dinero'))

    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                dinero = data.get('amount')
                nombre_cuota = data.get('quota_name')
            else:
                dinero = request.form['amount']
                nombre_cuota = request.form['quota_name']

            # Validar el monto de dinero
            dinero = float(dinero)
            if dinero <= 0:
                raise ValueError("El dinero debe ser positivo")

            # Actualizar la cuota
            cuota.amount = dinero
            cuota.quota_name = nombre_cuota
            db.session.commit()
            app.logger.info('Cuota actualizada con éxito')

            if request.is_json:
                return jsonify({"message": "Cuota actualizada con éxito"}), 200
            else:
                return redirect(url_for('dinero'))
        except ValueError as e:
            flash(str(e), 'error')
            if request.is_json:
                return jsonify({"error": str(e)}), 400
            return redirect(url_for('dinero'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = "Error al actualizar la cuota: " + str(e)
            app.logger.warning(error_msg)
            if request.is_json:
                return jsonify({"error": error_msg}), 500
            return redirect(url_for('dinero'))

    if request.is_json:
        return jsonify({
            "id": cuota.id,
            "user_id": cuota.user_id,
            "quota_name": cuota.quota_name,
            "amount": cuota.amount
        }), 200
    else:
        return render_template('editar_cuota.html', cuota=cuota)

################    USUARIOS        #####################
@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        try:
            # Verifica si la solicitud es JSON o un formulario
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                role = data.get('role')
            else:
                username = request.form['username']
                password = request.form['password']
                role = request.form['role']

            # Validar los datos
            if not username or not password or not role:
                raise ValueError("Todos los campos son obligatorios.")

            # Crear un nuevo usuario
            nuevo_usuario = User(
                username=username,
                # password_hash=generate_password_hash(password),  # Hashear contraseña
                password_hash=password,
                role=role
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            app.logger.info('Usuario creado con éxito')

            if request.is_json:
                return jsonify({"message": "Usuario creado con éxito"}), 201
            else:
                return redirect(url_for('login'))

        except ValueError as e:
            flash(str(e), 'error')
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al crear el usuario: {str(e)}"
            app.logger.warning(error_msg)
            if request.is_json:
                return jsonify({"error": error_msg}), 500

    # Obtener todos los usuarios
    usuarios = User.query.all()

    if request.is_json:
        usuarios_serializados = [
            {"id": u.id, "username": u.username, "role": u.role} for u in usuarios
        ]
        return jsonify(usuarios_serializados), 200
    else:
        return render_template('register.html', usuarios=usuarios)


@app.route('/usuarios/<string:username>', methods=['DELETE'])
@login_requerido
def eliminar_usuario_route(username):
    try:
        # Buscar el usuario por username
        usuario = User.query.filter_by(username=username).first()

        if not usuario:
            app.logger.warning('Usuario no encontrado')
            if request.is_json:
                return jsonify({"error": "Usuario no encontrado"}), 404
            return redirect(url_for('usuarios.usuarios'))

        # Eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()

        app.logger.info('Usuario eliminado con éxito')

        if request.is_json:
            return jsonify({"message": "Usuario eliminado con éxito"}), 200
        else:
            return redirect(url_for('usuarios.usuarios'))

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = f"Error al eliminar el usuario: {str(e)}"
        app.logger.warning(error_msg)
        if request.is_json:
            return jsonify({"error": error_msg}), 500
        return redirect(url_for('usuarios.usuarios'))


@app.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_usuario(user_id):
    usuario = User.query.get(user_id)

    if not usuario:
        app.logger.warning('Usuario no encontrado')
        if request.is_json:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return redirect(url_for('usuarios.usuarios'))

    if request.method == 'POST':
        try:
            # Verifica si la solicitud es JSON o un formulario
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
            else:
                username = request.form['username']
                password = request.form['password']

            # Validar los datos
            if not username:
                raise ValueError("El nombre de usuario es obligatorio.")

            # Actualizar datos del usuario
            usuario.username = username
            if password:  # Solo actualiza la contraseña si se proporciona
                usuario.password = generate_password_hash(password)
            db.session.commit()

            app.logger.info('Usuario actualizado con éxito')

            if request.is_json:
                return jsonify({"message": "Usuario actualizado con éxito"}), 200
            else:
                return redirect(url_for('usuarios.usuarios'))

        except ValueError as e:
            flash(str(e), 'error')
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al actualizar el usuario: {str(e)}"
            app.logger.warning(error_msg)
            if request.is_json:
                return jsonify({"error": error_msg}), 500

    if request.is_json:
        return jsonify({
            "id": usuario.id,
            "username": usuario.username,
            "role": usuario.role
        }), 200
    else:
        return render_template('editar_usuario.html', usuario=usuario)

##################      VOTACIONES      ###############
@app.route('/votaciones', methods=['GET', 'POST'])
@login_requerido
def votaciones():
    user_id = session.get('user_id')
    usuario_actual = User.query.get(user_id)  # Obtener los datos del usuario actual

    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            opciones = request.form['opciones'].split(',')  # Separar opciones por coma

            if not titulo or not opciones:
                raise ValueError("El título y las opciones son obligatorios.")

            # Crear una nueva votación
            nueva_votacion = Voting(title=titulo)
            db.session.add(nueva_votacion)
            db.session.flush()  # Obtener el ID antes de agregar las opciones

            # Crear las opciones asociadas a la votación
            for opcion in opciones:
                opcion = opcion.strip()  # Eliminar posibles espacios en blanco alrededor de cada opción
                if opcion:  # Verificar que la opción no esté vacía
                    nueva_opcion = Option(option_text=opcion, voting_id=nueva_votacion.id)
                    db.session.add(nueva_opcion)

            db.session.commit()

            app.logger.info('Votación creada con éxito')
            return redirect(url_for('votaciones'))

        except ValueError as e:
            flash(str(e), 'error')
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al crear la votación: {str(e)}"
            app.logger.warning(error_msg)

    # Obtener todas las votaciones
    votaciones = Voting.query.all()

    if request.headers.get("Accept") == "application/json":
        votaciones_serializadas = [
            {
                "id": v.id,
                "title": v.title,
                "options": [{"id": o.id, "text": o.option_text, "votes": len(o.votes)} for o in v.options],
            }
            for v in votaciones
        ]
        return jsonify(votaciones_serializadas), 200

    return render_template('votaciones.html', votaciones=votaciones, current_user=usuario_actual)


@app.route('/votaciones/<int:votacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_votacion(votacion_id):
    try:
        votacion = Voting.query.get(votacion_id)
        if not votacion:
            app.logger.warning("Votación no encontrada.")
            return redirect(url_for('votaciones'))

        db.session.delete(votacion)
        db.session.commit()

        app.logger.info('Votación eliminada con éxito')
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "success", "message": "Votación eliminada con éxito"}), 200
        return redirect(url_for('votaciones'))

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = f"Error al eliminar la votación: {str(e)}"
        app.logger.warning(error_msg)
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "error", "message": error_msg}), 500
        return redirect(url_for('votaciones'))


@app.route('/votaciones/<int:votacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_votacion(votacion_id):
    votacion = Voting.query.get(votacion_id)

    if not votacion:
        app.logger.info('Votación no encontrada.')
        return redirect(url_for('votaciones'))

    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            opciones = request.form['opciones'].splitlines()

            if not titulo or not opciones:
                raise ValueError("El título y las opciones son obligatorios.")

            # Actualizar la votación
            votacion.title = titulo
            db.session.query(Option).filter_by(voting_id=votacion.id).delete()  # Eliminar opciones anteriores
            db.session.flush()

            # Crear las nuevas opciones
            for opcion in opciones:
                nueva_opcion = Option(option_text=opcion, voting_id=votacion.id)
                db.session.add(nueva_opcion)

            db.session.commit()

            app.logger.info('Votación actualizada con éxito')
            return redirect(url_for('votaciones'))

        except ValueError as e:
            flash(str(e), 'error')
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = f"Error al actualizar la votación: {str(e)}"
            app.logger.warning(error_msg)

    return render_template('editar_votacion.html', votacion=votacion)


@app.route('/votaciones/votar/<int:opcion_id>', methods=['POST'])
@login_requerido
def votar_opcion(opcion_id):
    user_id = session.get('user_id')
    if not user_id:
        app.logger.warning("Usuario no autenticado.")
        return redirect(url_for('votaciones'))

    try:
        # Verificar si ya votó por esta opción
        voto_existente = Vote.query.filter_by(user_id=user_id, option_id=opcion_id).first()
        if voto_existente:
            app.logger.warning("Ya has votado por esta opción.")
            return redirect(url_for('votaciones'))

        # Registrar el voto
        nuevo_voto = Vote(user_id=user_id, option_id=opcion_id)
        db.session.add(nuevo_voto)
        db.session.commit()

        app.logger.info("Voto registrado con éxito.")
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "success", "message": "Voto registrado con éxito"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = f"Error al registrar el voto: {str(e)}"
        app.logger.warning(error_msg)
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "error", "message": error_msg}), 500

    return redirect(url_for('votaciones'))


###########     APP     #######################

# Verificar la conexión a la base de datos
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("Conexión exitosa a la base de datos")
    except Exception as e:
        print(f"Error al conectar: {e}")

class DefaultConfig:
    """
    Configuración por defecto para la aplicación Flask.
    """
    DEBUG = True
    TESTING = False
    SECRET_KEY = "paquito-flores-key"  # Clave secreta para sesiones
    JSON_SORT_KEYS = False

app.config.from_object(DefaultConfig)  # Carga la configuración
print(f"Clave secreta utilizada: {app.config['SECRET_KEY']}")
print(app.config)
 

if __name__ == "__main__":
    # Configuración verificada
    app.run(host="0.0.0.0", port=5000, debug=True)