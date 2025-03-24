from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Cliente
from forms import ClienteForm

clientes_bp = Blueprint('clientes', __name__, template_folder='../templates')

@clientes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ClienteForm(request.form)
    if request.method == 'POST' and form.validate():
        # Si se envía un campo oculto 'id', se trata de una edición
        cliente_id = request.form.get('id')
        if cliente_id:
            cliente = Cliente.query.get(cliente_id)
            cliente.nombre = form.nombre.data
            cliente.telefono = form.telefono.data
            cliente.direccion = form.direccion.data
            flash(f'Cliente {cliente.nombre} actualizado.', 'success')
        else:
            cliente = Cliente(
                nombre=form.nombre.data,
                telefono=form.telefono.data,
                direccion=form.direccion.data
            )
            db.session.add(cliente)
            flash(f'Cliente {form.nombre.data} creado exitosamente.', 'success')
        db.session.commit()
        return redirect(url_for('clientes.index'))
    clientes = Cliente.query.filter_by(activo=True).all()
    return render_template('clientes.html', form=form, clientes=clientes)

@clientes_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    cliente = Cliente.query.get(id)
    form = ClienteForm(obj=cliente)
    return render_template('clientes.html', form=form, cliente=cliente, editar=True, clientes=Cliente.query.filter_by(activo=True).all())

@clientes_bp.route('/eliminar/<int:id>')
def eliminar(id):
    cliente = Cliente.query.get(id)
    # Eliminación lógica: actualiza 'activo' a False
    cliente.activo = False
    db.session.commit()
    flash('Cliente eliminado lógicamente.', 'success')
    return redirect(url_for('clientes.index'))
