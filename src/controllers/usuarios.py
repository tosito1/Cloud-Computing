from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from services.user_service import (
    insertar_usuario_service,
    obtener_usuarios_service,
    eliminar_usuario_service,
    obtener_usuario_por_id,
    actualizar_usuario_service
)
from controllers.auth import login_requerido

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/', methods=['GET', 'POST'])
#@login_requerido
def usuarios():
    if request.method == 'POST':
        # Verifica si la solicitud es JSON o un formulario
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
        # Lógica para insertar un usuario
        insertar_usuario_service(username, password,role)
        flash('Usuario creado con éxito')

        if request.is_json:
            return jsonify({"message": "Usuario creado con éxito"}), 201
        else:
            return redirect(url_for('auth.login'))

    #usuarios = obtener_usuarios()
    if request.is_json:
        return jsonify(usuarios), 200
    else:
        return render_template('register.html')

@usuarios_bp.route('/<int:user_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_usuario_route(user_id):
    eliminar_usuario_service(user_id)  # Lógica para eliminar un usuario
    flash('Usuario eliminado con éxito')

    if request.is_json:
        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    else:
        return redirect(url_for('usuarios.usuarios'))

@usuarios_bp.route('/<int:user_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_usuario(user_id):
    usuario = obtener_usuario_por_id(user_id)
    if request.method == 'POST':
        # Verifica si la solicitud es JSON o un formulario
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form['username']
            password = request.form['password']

        # Lógica para actualizar el usuario
        actualizar_usuario_service(user_id, username, password)
        flash('Usuario actualizado con éxito')

        if request.is_json:
            return jsonify({"message": "Usuario actualizado con éxito"}), 200
        else:
            return redirect(url_for('usuarios.usuarios'))

    if request.is_json:
        return jsonify(usuario), 200
    else:
        return render_template('editar_usuario.html', usuario=usuario)
