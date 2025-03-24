from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Usuario
from flask_login import login_user, logout_user, login_required
from flask_wtf.csrf import generate_csrf

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and user.password == password:
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
