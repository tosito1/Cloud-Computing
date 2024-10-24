from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from dbs.db_money import insertar_cuota, obtener_cuotas, insertar_multa, obtener_multas, actualizar_cuota, eliminar_cuota
from controllers.auth import login_requerido

dinero_bp = Blueprint('dinero', __name__)

@dinero_bp.route('/dinero', methods=['GET', 'POST'])
@login_requerido
def dinero():
    if request.method == 'POST':
        monto = request.form['monto']
        insertar_cuota(monto)
        flash('Cuota creada con éxito')
        return redirect(url_for('dinero.dinero'))

    cuotas = obtener_cuotas()
    multas = obtener_multas()
    return render_template('dinero.html', cuotas=cuotas, multas=multas)

@dinero_bp.route('/dinero/cuota/<int:cuota_id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_cuota(cuota_id):
    cuota = obtener_cuota_por_id(cuota_id)
    if request.method == 'POST':
        monto = request.form['monto']
        actualizar_cuota(cuota_id, monto)
        flash('Cuota actualizada con éxito')
        return redirect(url_for('dinero.dinero'))
    return render_template('editar_cuota.html', cuota=cuota)

@dinero_bp.route('/dinero/multa', methods=['POST'])
@login_requerido
def agregar_multa():
    monto = request.form['monto']
    insertar_multa(monto)
    flash('Multa creada con éxito')
    return redirect(url_for('dinero.dinero'))
