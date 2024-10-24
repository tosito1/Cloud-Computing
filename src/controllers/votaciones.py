from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from dbs.db_voting import insertar_votacion, obtener_votaciones, actualizar_votacion, eliminar_votacion
from controllers.auth import login_requerido

votaciones_bp = Blueprint('votaciones', __name__)

@votaciones_bp.route('/votaciones', methods=['GET', 'POST'])
@login_requerido
def votaciones():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        insertar_votacion(titulo, descripcion)
        flash('Votación creada con éxito')
        return redirect(url_for('votaciones.votaciones'))

    votaciones = obtener_votaciones()
    return render_template('votaciones.html', votaciones=votaciones)

@votaciones_bp.route('/votaciones/<int:votacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_votacion(votacion_id):
    eliminar_votacion(votacion_id)
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
