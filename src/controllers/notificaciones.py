import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from controllers.auth import login_requerido

notificaciones_bp = Blueprint('notificaciones', __name__)

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import datetime
from services.notification_service import (
    insertar_notificacion_service,
    obtener_notificaciones_service,
    eliminar_notificacion_service,
    actualizar_notificacion_service
)
from controllers.auth import login_requerido
from services.user_service import obtener_usuario_id_service

# Definimos el Blueprint para las notificaciones
notificaciones_bp = Blueprint('notificaciones', __name__)

# Ruta para mostrar y crear notificaciones
@notificaciones_bp.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    user_id = session.get('user_id')
    usuario_actual = obtener_usuario_id_service(user_id)  # Obtener los datos del usuario actual

    if request.method == 'POST':
        titulo = request.form['titulo']
        texto = request.form['texto']
        # Insertar la notificación en la base de datos
        insertar_notificacion_service(titulo, texto, user_id, datetime.date.today())
        flash('Notificación creada con éxito')
        return redirect(url_for('notificaciones.notificaciones'))

    # Obtener todas las notificaciones para mostrarlas
    notificaciones = obtener_notificaciones_service()
    return render_template('notificaciones.html', notificaciones=notificaciones, current_user=usuario_actual)

# Ruta para eliminar notificaciones
@notificaciones_bp.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    eliminar_notificacion_service(notificacion_id)  # Llamada al servicio para eliminar la notificación
    flash('Notificación eliminada con éxito')
    return redirect(url_for('notificaciones.notificaciones'))

# Ruta para editar una notificación (comentada por ahora)
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
