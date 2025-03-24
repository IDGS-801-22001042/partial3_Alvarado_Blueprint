from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Venta, Usuario  
import forms
import os
from datetime import datetime
from sqlalchemy import extract
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
app.secret_key = "Papitas Con Salsa"

#INICIALIZA FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrar Blueprints
from blueprints.auth import auth_bp
from blueprints.clientes import clientes_bp
from blueprints.proveedores import proveedores_bp

app.register_blueprint(auth_bp, url_prefix='/login')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(proveedores_bp, url_prefix='/proveedores')

@login_manager.user_loader#Función de carga del usuario
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # Cambiado de 'usuario' a 'username'
        password = request.form['password']  # Se puede mantener 'password'
        user = Usuario.query.filter_by(usuario=username).first()  # Se filtra por el campo 'usuario' del modelo
        if user and user.contrasenia == password:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Credenciales inválidas', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))


# Archivo temporal 
TEMP_FILE = 'pizzas_temp.txt'

def read_pizzas_temp():
    pizzas = []
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    tamano, jamon_str, pina_str, champi_str, num_str, sub_str = parts
                    jamon = (jamon_str == 'True')
                    pina = (pina_str == 'True')
                    champi = (champi_str == 'True')
                    numero = int(num_str)
                    subtotal = float(sub_str)
                    ing_list = []
                    if jamon: ing_list.append('Jamón')
                    if pina: ing_list.append('Piña')
                    if champi: ing_list.append('Champiñones')
                    pizza_dict = {
                        'tamano': tamano,
                        'ingredientes': ', '.join(ing_list),
                        'jamon': jamon,
                        'pina': pina,
                        'champi': champi,
                        'numero': numero,
                        'subtotal': subtotal
                    }
                    pizzas.append(pizza_dict)
    return pizzas

def write_pizzas_temp(pizzas):
    with open(TEMP_FILE, 'w') as f:
        for p in pizzas:
            line = f"{p['tamano']}|{p['jamon']}|{p['pina']}|{p['champi']}|{p['numero']}|{p['subtotal']}\n"
            f.write(line)

def calcular_subtotal(tamano, jamon, pina, champi, numero):
    precios_tamano = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
    precio_base = precios_tamano.get(tamano, 50)
    precio_ingredientes = (10 if jamon else 0) + (10 if pina else 0) + (10 if champi else 0)
    return (precio_base + precio_ingredientes) * numero

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
   
    pizza_form = forms.PizzaForm(request.form)
    ventas_form = forms.ConsultaVentasForm(request.form)
    
    pizzas = read_pizzas_temp()
    subtotal_general = sum([p['subtotal'] for p in pizzas])
    
    ventas_result = []
    total_dia_mes = 0
    agrupado = {}

    if request.method == 'POST':

        if 'tamano' in request.form:
            pizza_form.tamano.data = request.form['tamano']

        
        if pizza_form.btn_agregar.data or pizza_form.btn_quitar.data or pizza_form.btn_terminar.data:
            if pizza_form.btn_agregar.data:
                
                if not pizza_form.validate():
                    flash("Por favor, corrige los errores en el formulario.", "error")
                    return render_template('index.html', pizza_form=pizza_form, ventas_form=ventas_form,
                                           pizzas=pizzas, subtotal_general=subtotal_general,
                                           ventas=ventas_result, agrupado=agrupado, total_dia_mes=total_dia_mes)
                
                # Almacenar datos del cliente en sesión 
                session['nombre'] = pizza_form.nombre.data
                session['direccion'] = pizza_form.direccion.data
                session['telefono'] = pizza_form.telefono.data
                session['fecha'] = pizza_form.fecha.data.strftime('%Y-%m-%d') if pizza_form.fecha.data else ''

                # Agregar la pizza
                tamano = pizza_form.tamano.data
                jamon = pizza_form.jamon.data
                pina = pizza_form.pina.data
                champi = pizza_form.champi.data
                numero = pizza_form.numero_pizzas.data

                st = calcular_subtotal(tamano, jamon, pina, champi, numero)
                new_item = {
                    'tamano': tamano,
                    'jamon': jamon,
                    'pina': pina,
                    'champi': champi,
                    'numero': numero,
                    'subtotal': st
                }
                ing_list = []
                if jamon: ing_list.append('Jamón')
                if pina: ing_list.append('Piña')
                if champi: ing_list.append('Champiñones')
                new_item['ingredientes'] = ', '.join(ing_list)

                pizzas.append(new_item)
                write_pizzas_temp(pizzas)
                flash('Pizza agregada al pedido.', 'success')
                return redirect(url_for('index'))

            elif pizza_form.btn_quitar.data:
                if pizzas:
                    pizzas.pop()
                    write_pizzas_temp(pizzas)
                    flash('Última pizza eliminada del pedido.', 'info')
                else:
                    flash('No hay pizzas para eliminar.', 'warning')
                return redirect(url_for('index'))

            elif pizza_form.btn_terminar.data:
                if pizzas:
                    total = sum([p['subtotal'] for p in pizzas])
                    
                    nombre = pizza_form.nombre.data or session.get('nombre', '')
                    direccion = pizza_form.direccion.data or session.get('direccion', '')
                    telefono = pizza_form.telefono.data or session.get('telefono', '')
                    if pizza_form.fecha.data:
                        fecha = pizza_form.fecha.data
                    else:
                        try:
                            fecha = datetime.strptime(session.get('fecha', ''), '%Y-%m-%d').date()
                        except Exception:
                            fecha = None

                    nueva_venta = Venta(
                        nombre=nombre,
                        direccion=direccion,
                        telefono=telefono,
                        fecha_pedido=fecha,
                        total=total
                    )
                    db.session.add(nueva_venta)
                    db.session.commit()
                    flash(f"Pedido terminado. Total a pagar: ${total}", 'success')
                    write_pizzas_temp([])
                    session.pop('nombre', None)
                    session.pop('direccion', None)
                    session.pop('telefono', None)
                    session.pop('fecha', None)
                else:
                    flash("No hay pizzas en el pedido.", 'error')
                return redirect(url_for('index'))
        
        # formulario de consulta de ventas
        elif ventas_form.btn_buscar.data and ventas_form.validate():
            tipo = ventas_form.tipo_busqueda.data
            fecha = ventas_form.fecha_busqueda.data  
            if tipo == 'dia':
                ventas_result = Venta.query.filter(Venta.fecha_pedido == fecha).all()
            else:
                ventas_result = Venta.query.filter(
                    extract('month', Venta.fecha_pedido) == fecha.month,
                    extract('year', Venta.fecha_pedido) == fecha.year
                ).all()
            total_dia_mes = sum(v.total for v in ventas_result)
            for v in ventas_result:
                agrupado[v.nombre] = agrupado.get(v.nombre, 0) + v.total

    
    if request.method == 'GET':
        if 'nombre' in session:
            pizza_form.nombre.data = session.get('nombre')
        if 'direccion' in session:
            pizza_form.direccion.data = session.get('direccion')
        if 'telefono' in session:
            pizza_form.telefono.data = session.get('telefono')
        if 'fecha' in session:
            try:
                pizza_form.fecha.data = datetime.strptime(session.get('fecha'), '%Y-%m-%d')
            except:
                pass

    return render_template('index.html', pizza_form=pizza_form, ventas_form=ventas_form,
                           pizzas=pizzas, subtotal_general=subtotal_general,
                           ventas=ventas_result, agrupado=agrupado, total_dia_mes=total_dia_mes)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3000)
