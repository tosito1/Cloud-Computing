from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from dbs.db_user import obtener_usuario_por_id
from dbs.db_voting import eliminar_votacion_db, insertar_votacion, obtener_votaciones, actualizar_votacion, registrar_voto
from controllers.auth import login_requerido

votaciones_bp = Blueprint('votaciones', __name__)

@votaciones_bp.route('/votaciones', methods=['GET', 'POST'])
@login_requerido
def votaciones():
    user_id = session.get('user_id')
    usuario_actual = obtener_usuario_por_id(user_id)
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['opciones']
        insertar_votacion(titulo, descripcion)
        flash('Votación creada con éxito')
        return redirect(url_for('votaciones.votaciones'))

    votaciones = obtener_votaciones()
    return render_template('votaciones.html', votaciones=votaciones, current_user=usuario_actual)

@votaciones_bp.route('/votaciones/<int:votacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_votacion(votacion_id):
    eliminar_votacion_db(votacion_id)
    flash('Votación eliminada con éxito')
    return redirect(url_for('votaciones.votaciones'))

@votaciones_bp.route('/votaciones/<int:votacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_votacion(votacion_id):
    votacion = obtener_votaciones(votacion_id)
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        actualizar_votacion(votacion_id, titulo, descripcion)
        flash('Votación actualizada con éxito')
        return redirect(url_for('votaciones.votaciones'))
    return render_template('editar_votacion.html', votacion=votacion)


@votaciones_bp.route('/votaciones/votar/<int:opcion_id>', methods=['POST'])
@login_requerido
def votar_opcion(opcion_id):
    user_id = session.get('user_id')  # Obtén el ID del usuario actual
    if user_id:
        exito = registrar_voto(opcion_id, user_id)  # Registra el voto
        if exito:
            flash("Voto registrado con éxito.")
        else:
            flash("Error al registrar el voto. Es posible que ya hayas votado.")
    return redirect(url_for('votaciones.votaciones'))
