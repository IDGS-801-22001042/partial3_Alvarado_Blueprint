from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Usuario
from flask_login import login_user, logout_user, login_required
from flask_wtf.csrf import generate_csrf
from forms import RegistrationForm

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(usuario=username).first()
        if user and user.contrasenia == password:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Credenciales inválidas', 'error')
    csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm  # Importa aquí el formulario de registro
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        existing_user = Usuario.query.filter_by(usuario=form.username.data).first()
        if existing_user:
            flash('El usuario ya existe.', 'error')
            return render_template('register.html', form=form)
        new_user = Usuario(
            usuario=form.username.data,
            contrasenia=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado exitosamente. Por favor, inicie sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
