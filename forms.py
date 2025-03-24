from wtforms import Form, validators, BooleanField, StringField, DateField, SelectField, IntegerField, RadioField, SubmitField

class PizzaForm(Form):
    # Datos de la pizza
    tamano = SelectField("Tamaño", choices=[('Chica', 'Chica ($50)'), ('Mediana', 'Mediana ($70)'), ('Grande', 'Grande ($120)')], 
                         validators=[validators.DataRequired(message='Selecciona un tamaño')])
    jamon = BooleanField("Jamón")
    pina = BooleanField("Piña")
    champi = BooleanField("Champiñones")
    numero_pizzas = IntegerField("Cantidad", validators=[
        validators.DataRequired(message='Campo requerido'),
        validators.NumberRange(min=1, max=20)
    ])
    # Datos del cliente
    nombre = StringField("Nombre Completo", [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=4, max=100)
    ])
    direccion = StringField("Dirección", [
        validators.DataRequired(message='Campo requerido')
    ])
    telefono = StringField("Teléfono", [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=10, max=15)
    ])
    fecha = DateField("Fecha", format='%Y-%m-%d',
        validators=[ validators.DataRequired(message='Selecciona una fecha') ])
    # Botones de acción
    btn_agregar = SubmitField("Agregar")
    btn_quitar = SubmitField("Quitar")
    btn_terminar = SubmitField("Terminar")


class ConsultaVentasForm(Form):
    tipo_busqueda = RadioField("Tipo de reporte", choices=[('dia', 'Día'), ('mes', 'Mes')], 
                                 validators=[validators.DataRequired(message='Selecciona un tipo')])
    fecha_busqueda = DateField("Fecha", format='%Y-%m-%d', validators=[
        validators.DataRequired(message='Selecciona una fecha')
    ])
    btn_buscar = SubmitField("Buscar")


class ClienteForm(Form):
    nombre = StringField("Nombre", [validators.DataRequired(message='Campo requerido'),
                                    validators.Length(min=4, max=150)])
    telefono = StringField("Teléfono", [validators.DataRequired(message='Campo requerido'),
                                        validators.Length(min=8, max=50)])
    direccion = StringField("Dirección", [validators.DataRequired(message='Campo requerido')])
    btn_guardar = SubmitField("Guardar")

class ProveedorForm(Form):
    nombre = StringField("Nombre", [validators.DataRequired(message='Campo requerido'),
                                    validators.Length(min=4, max=150)])
    telefono = StringField("Teléfono", [validators.DataRequired(message='Campo requerido'),
                                        validators.Length(min=8, max=50)])
    empresa = StringField("Empresa", [validators.DataRequired(message='Campo requerido')])
    btn_guardar = SubmitField("Guardar")