from main import db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    notifications = db.relationship("Notification", backref="president", lazy="dynamic")
    quotas = db.relationship("Quota", backref="user", lazy="dynamic")
    fines = db.relationship("Fine", backref="user", lazy="dynamic")
    votes = db.relationship("Vote", backref="user", lazy="dynamic")


class Notification(db.Model):
    __tablename__ = "notificationes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    president_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Voting(db.Model):
    __tablename__ = "votaciones"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    options = db.relationship('Option', backref='votacion', cascade='all, delete')


class Option(db.Model):
    __tablename__ = 'opciones'
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String, nullable=False)
    voting_id = db.Column(db.Integer, db.ForeignKey('votaciones.id'), nullable=False)
    voting = db.relationship('Voting', backref='opciones', lazy=True)
    votes = db.relationship('Vote', backref='opciones', lazy=True)



class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("opciones.id"), nullable=False)


class Quota(db.Model):
    __tablename__ = "cuotas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, nullable=False, default="pendiente")  # Agrega un valor predeterminado
    fine_id = db.Column(db.Integer, db.ForeignKey("multas.id"))



class Fine(db.Model):
    __tablename__ = "multas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    quota_id = db.Column(db.Integer, db.ForeignKey("cuotas.id", ondelete="SET NULL"))
    date = db.Column(db.DateTime, default=datetime.utcnow)