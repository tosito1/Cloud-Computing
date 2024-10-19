from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    presidente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    presidente = db.relationship('User', backref='notificaciones')

class Votacion(db.Model):
    __tablename__ = 'votacion'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    opciones = db.relationship('Opcion', backref='votacion', lazy=True)
    fecha = db.Column(db.DateTime, nullable=False)

class Opcion(db.Model):
    __tablename__ = 'opcion'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(150), nullable=False)
    votos = db.Column(db.Integer, default=0)
    votacion_id = db.Column(db.Integer, db.ForeignKey('votacion.id'), nullable=False)
