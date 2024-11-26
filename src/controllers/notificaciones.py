import datetime
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, session
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

@notificaciones_bp.route('/notificaciones', methods=['GET', 'POST'])
@login_requerido
def notificaciones():
    user_id = session.get('user_id')
    usuario_actual = obtener_usuario_id_service(user_id)  # Obtener los datos del usuario actual

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        if not titulo or not texto:
            flash('Título y texto son obligatorios', 'error')
            return redirect(url_for('notificaciones.notificaciones'))

        # Insertar la notificación en la base de datos
        insertar_notificacion_service(titulo, texto, user_id, datetime.datetime.now())
        flash('Notificación creada con éxito')
        return redirect(url_for('notificaciones.notificaciones'))

    # Obtener todas las notificaciones
    notificaciones = obtener_notificaciones_service()

    # Si la solicitud espera JSON
    if request.headers.get("Accept") == "application/json":
        return jsonify(notificaciones)

    # Renderizar la plantilla HTML
    return render_template('notificaciones.html', notificaciones=notificaciones, current_user=usuario_actual)


# Ruta para eliminar notificaciones
@notificaciones_bp.route('/notificaciones/<int:notificacion_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_notificacion(notificacion_id):
    try:
        eliminar_notificacion_service(notificacion_id)  # Llamada al servicio para eliminar la notificación
        flash('Notificación eliminada con éxito')

        # Respuesta en JSON para los tests
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "success", "message": "Notificación eliminada con éxito"}), 200

        # Redirigir a la página de notificaciones
        return redirect(url_for('notificaciones.notificaciones'))

    except Exception as e:
        # Manejar errores en JSON
        if request.headers.get("Accept") == "application/json":
            return jsonify({"status": "error", "message": f"Error al eliminar la notificación: {str(e)}"}), 500

        flash(f'Error al eliminar la notificación: {str(e)}', 'error')
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
