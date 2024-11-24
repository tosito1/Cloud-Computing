from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from services.voting_service import (
    insertar_votacion_service,
    obtener_votaciones_service,
    eliminar_votacion_service,
    actualizar_votacion_service,
    registrar_voto_service
)
from services.user_service import obtener_usuario_id_service
from controllers.auth import login_requerido

# Definimos el Blueprint para las votaciones
votaciones_bp = Blueprint('votaciones', __name__)

# Ruta para mostrar y crear votaciones
@votaciones_bp.route('/votaciones', methods=['GET', 'POST'])
@login_requerido
def votaciones():
    user_id = session.get('user_id')
    usuario_actual = obtener_usuario_id_service(user_id)  # Obtener los datos del usuario actual

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['opciones']  # "opciones" sería el texto con las alternativas
        insertar_votacion_service(titulo, descripcion)  # Insertar votación en la base de datos
        flash('Votación creada con éxito')
        return redirect(url_for('votaciones.votaciones'))

    # Obtener todas las votaciones disponibles
    votaciones = obtener_votaciones_service()
    return render_template('votaciones.html', votaciones=votaciones, current_user=usuario_actual)

# Ruta para eliminar una votación
@votaciones_bp.route('/votaciones/<int:votacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_votacion(votacion_id):
    eliminar_votacion_service(votacion_id)  # Eliminar votación de la base de datos
    flash('Votación eliminada con éxito')
    return redirect(url_for('votaciones.votaciones'))

# Ruta para editar una votación
@votaciones_bp.route('/votaciones/<int:votacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_votacion(votacion_id):
    votacion = obtener_votaciones_service(votacion_id)  # Obtener la votación que se desea editar
    if not votacion:
        flash('Votación no encontrada.')
        return redirect(url_for('votaciones.votaciones'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['opciones']  # "opciones" sería el nuevo texto con las alternativas
        actualizar_votacion_service(votacion_id, titulo, descripcion)  # Actualizar votación en la base de datos
        flash('Votación actualizada con éxito')
        return redirect(url_for('votaciones.votaciones'))

    return render_template('editar_votacion.html', votacion=votacion)

# Ruta para registrar un voto en una opción de votación
@votaciones_bp.route('/votaciones/votar/<int:opcion_id>', methods=['POST'])
@login_requerido
def votar_opcion(opcion_id):
    user_id = session.get('user_id')  # Obtener el ID del usuario actual
    if user_id:
        exito = registrar_voto_service(opcion_id, user_id)  # Intentar registrar el voto
        if exito:
            flash("Voto registrado con éxito.")
        else:
            flash("Error al registrar el voto. Es posible que ya hayas votado en esta opción.")
    return redirect(url_for('votaciones.votaciones'))
