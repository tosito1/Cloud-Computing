from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from services.dinero_service import (
    insertar_cuota_service,
    obtener_cuotas_service,
    eliminar_cuota_service,
    obtener_cuota_por_id_service,
    #actualizar_cuota
)
from services.user_service import (
    obtener_usuarios_service
)
from controllers.auth import login_requerido

dinero_bp = Blueprint('dinero', __name__, url_prefix='/dinero')

@dinero_bp.route('/', methods=['GET', 'POST'])
@login_requerido
def cuotas():
    if request.method == 'POST':
        try:
            # Verifica si la solicitud es JSON o un formulario
            if request.is_json:
                data = request.get_json()
                dinero = data.get('amount')
                nombre_cuota = data.get('quota_name')
                user_id = data.get('user_id')
            else:
                dinero = request.form['amount']
                nombre_cuota = request.form['quota_name']
                user_id = request.form['user_id']

            # Validar el monto de dinero
            dinero = float(dinero)  # Convertir a float
            if dinero <= 0:
                raise ValueError("El monto debe ser positivo")

            # Lógica para insertar una nueva cuota
            insertar_cuota_service(user_id, nombre_cuota, dinero)
            flash('Cuota creada con éxito')

            if request.is_json:
                return jsonify({"message": "Cuota creada con éxito"}), 201
            else:
                return redirect(url_for('dinero.cuotas'))

        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('dinero.cuotas'))

    # Obtener cuotas y usuarios
    usuarios = obtener_usuarios_service()
    cuotas = obtener_cuotas_service()
    if request.headers.get("Accept") == "application/json":
        return jsonify(cuotas), 200
    else:
        return render_template('dinero.html', cuotas=cuotas, usuarios=usuarios)

@dinero_bp.route('/<int:cuota_id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_cuota_route(cuota_id):
    eliminar_cuota_service(cuota_id)  # Lógica para eliminar una cuota
    flash('Cuota eliminada con éxito')

    if request.is_json:
        return jsonify({"message": "Cuota eliminada con éxito"}), 200
    else:
        return redirect(url_for('dinero.cuotas'))

@dinero_bp.route('/<int:cuota_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_cuota(cuota_id):
    cuota = obtener_cuota_por_id_service(cuota_id)
    if request.method == 'POST':
        # Verifica si la solicitud es JSON o un formulario
        if request.is_json:
            data = request.get_json()
            dinero = data.get('amount')
            nombre_cuota = data.get('quota_name')
        else:
            dinero = request.form['amount']
            nombre_cuota = request.form['quota_name']

        # Lógica para actualizar la cuota
        #actualizar_cuota_service(cuota_id, monto, descripcion)
        flash('Cuota actualizada con éxito')

        if request.is_json:
            return jsonify({"message": "Cuota actualizada con éxito"}), 200
        else:
            return redirect(url_for('dinero.cuotas'))

    if request.is_json:
        return jsonify(cuota), 200
    else:
        return render_template('editar_cuota.html', cuota=cuota)
