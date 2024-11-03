from flask import Blueprint, render_template, redirect, url_for, request, flash
from dbs.db_money import insertar_cuota, obtener_cuotas, insertar_multa, obtener_multas
from controllers.auth import login_requerido
from dbs.db_user import obtener_usuarios

dinero_bp = Blueprint('dinero', __name__)

@dinero_bp.route('/dinero', methods=['GET', 'POST'])
@login_requerido
def dinero():
    if request.method == 'POST':
        user_id = request.form['user_id']
        amount = request.form['amount']
        quota_name = request.form['quota_name']  # Nombre de la cuota
        fine_amount = request.form.get('multa_amount')  # Monto de la multa (opcional)

        # Llama a insertar_cuota y pasa todos los parámetros necesarios
        if insertar_cuota(user_id, quota_name, amount, fine_amount):
            flash('Pago registrado con éxito.')
        else:
            flash('Error al registrar el pago.')
        return redirect(url_for('dinero.dinero'))

    # Obtener las cuotas y multas para mostrarlas en el formulario
    cuotas = obtener_cuotas()
    multas = obtener_multas()
    usuarios = obtener_usuarios()  # Función que recupera todos los usuarios
    return render_template('dinero.html', cuotas=cuotas, multas=multas, usuarios=usuarios)

# @dinero_bp.route('/dinero/cuota/<int:cuota_id>/editar', methods=['GET', 'POST'])
# @login_requerido
# def editar_cuota(cuota_id):
#     cuota = obtener_cuota_por_id(cuota_id)
#     if request.method == 'POST':
#         monto = request.form['monto']
#         actualizar_cuota(cuota_id, monto)
#         flash('Cuota actualizada con éxito')
#         return redirect(url_for('dinero.dinero'))
#     return render_template('editar_cuota.html', cuota=cuota)

@dinero_bp.route('/dinero/multa', methods=['POST'])
@login_requerido
def agregar_multa():
    monto = request.form['monto']
    insertar_multa(monto)
    flash('Multa creada con éxito')
    return redirect(url_for('dinero.dinero'))
