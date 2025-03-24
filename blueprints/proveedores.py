from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proveedor
from forms import ProveedorForm

proveedores_bp = Blueprint('proveedores', __name__, template_folder='../templates')

@proveedores_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ProveedorForm(request.form)
    if request.method == 'POST' and form.validate():
        proveedor_id = request.form.get('id')
        if proveedor_id:
            proveedor = Proveedor.query.get(proveedor_id)
            proveedor.nombre = form.nombre.data
            proveedor.telefono = form.telefono.data
            proveedor.empresa = form.empresa.data
            flash(f'Proveedor {proveedor.nombre} actualizado.', 'success')
        else:
            proveedor = Proveedor(
                nombre=form.nombre.data,
                telefono=form.telefono.data,
                empresa=form.empresa.data
            )
            db.session.add(proveedor)
            flash(f'Proveedor {form.nombre.data} creado exitosamente.', 'success')
        db.session.commit()
        return redirect(url_for('proveedores.index'))
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('proveedores.html', form=form, proveedores=proveedores)

@proveedores_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    proveedor = Proveedor.query.get(id)
    form = ProveedorForm(obj=proveedor)
    return render_template('proveedores.html', form=form, proveedor=proveedor, editar=True, proveedores=Proveedor.query.filter_by(activo=True).all())

@proveedores_bp.route('/eliminar/<int:id>')
def eliminar(id):
    proveedor = Proveedor.query.get(id)
    proveedor.activo = False
    db.session.commit()
    flash('Proveedor eliminado lógicamente.', 'success')
    return redirect(url_for('proveedores.index'))
