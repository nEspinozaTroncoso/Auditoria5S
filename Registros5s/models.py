from Registros5s import db
from datetime import datetime


class Auditoria(db.Model):
    __tablename__ = "auditorias"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    responsable = db.Column(db.String(100))
    area = db.Column(db.String(100))  # <-- Agrega este campo
    total = db.Column(db.Float)
    respuestas = db.relationship("Respuesta", backref="auditoria", lazy=True)


class Respuesta(db.Model):
    __tablename__ = "respuestas"
    id = db.Column(db.Integer, primary_key=True)
    auditoria_id = db.Column(db.Integer, db.ForeignKey("auditorias.id"), nullable=False)
    seccion = db.Column(db.String(50))
    pregunta = db.Column(db.String(255))
    puntaje = db.Column(db.Integer)
    imagen_path = db.Column(db.String(255), nullable=True)
