from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from dbs.db_user import insertar_usuario, obtener_usuarios, eliminar_usuario, obtener_usuario_por_id, actualizar_usuario
from controllers.auth import login_requerido

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET', 'POST'])
@login_requerido
def usuarios():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insertar_usuario(username, password)  # Función para insertar usuario
        flash('Usuario creado con éxito')
        return redirect(url_for('usuarios.usuarios'))

    usuarios = obtener_usuarios()  # Obtener todos los usuarios
    return render_template('usuarios.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/<int:user_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_usuario_route(user_id):
    eliminar_usuario(user_id)  # Función para eliminar usuario
    flash('Usuario eliminado con éxito')
    return redirect(url_for('usuarios.usuarios'))

@usuarios_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_usuario(user_id):
    usuario = obtener_usuario_por_id(user_id)  # Obtén el usuario a editar
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        actualizar_usuario(user_id, username, password)  # Función para actualizar usuario
        flash('Usuario actualizado con éxito')
        return redirect(url_for('usuarios.usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)
