from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(50))
    fecha_pedido = db.Column(db.Date)
    total = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia = db.Column(db.String(200), nullable=False)
    
    def get_id(self):
        return str(self.idUsuario)
