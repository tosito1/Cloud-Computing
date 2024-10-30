import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from src.dbs.db_notification import eliminar_notificacion_db, insertar_notificacion, obtener_notificaciones, actualizar_notificacion
from src.controllers.auth import login_requerido
from src.controllers.usuarios import obtener_usuario_por_id 

notificaciones_bp = Blueprint('notificaciones', __name__)

@notificaciones_bp.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    user_id = session.get('user_id')
    usuario_actual = obtener_usuario_por_id(user_id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        insertar_notificacion(titulo, texto, user_id, datetime.date.today())
        flash('Notificacion creada con exito')
        return redirect(url_for('notificaciones.notificaciones'))

    notificaciones = obtener_notificaciones()
    return render_template('notificaciones.html', notificaciones=notificaciones, current_user=usuario_actual)


@notificaciones_bp.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    eliminar_notificacion_db(notificacion_id)
    flash('Notificacion eliminada con exito')
    return redirect(url_for('notificaciones.notificaciones'))

# @notificaciones_bp.route('/notificaciones/<int:notificacion_id>/editar', methods=['GET', 'POST'])
# @login_requerido
# def editar_notificacion(notificacion_id):
#     notificacion = obtener_notificacion_por_id(notificacion_id)
#     if request.method == 'POST':
#         titulo = request.form['titulo']
#         texto = request.form['texto']
#         actualizar_notificacion(notificacion_id, titulo, texto)
#         flash('Notificación actualizada con éxito')
#         return redirect(url_for('notificaciones.notificaciones'))
#     return render_template('editar_notificacion.html', notificacion=notificacion)
