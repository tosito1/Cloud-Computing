from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from dbs.db_notification import insertar_notificacion, obtener_notificaciones, actualizar_notificacion, eliminar_notificacion
from controllers.auth import login_requerido

notificaciones_bp = Blueprint('notificaciones', __name__)

@notificaciones_bp.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        insertar_notificacion(titulo, texto, session['user_id'])
        flash('Notificación creada con éxito')
        return redirect(url_for('notificaciones.notificaciones'))

    notificaciones = obtener_notificaciones()
    return render_template('notificaciones.html', notificaciones=notificaciones)

@notificaciones_bp.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    eliminar_notificacion(notificacion_id)
    flash('Notificación eliminada con éxito')
    return redirect(url_for('notificaciones.notificaciones'))

@notificaciones_bp.route('/notificaciones/<int:notificacion_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_notificacion(notificacion_id):
    notificacion = obtener_notificacion_por_id(notificacion_id)
    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        actualizar_notificacion(notificacion_id, titulo, texto)
        flash('Notificación actualizada con éxito')
        return redirect(url_for('notificaciones.notificaciones'))
    return render_template('editar_notificacion.html', notificacion=notificacion)
