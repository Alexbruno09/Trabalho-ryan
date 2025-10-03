from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    registros = db.relationship("Registro", backref="aluno", lazy=True)


class Registro(db.Model):
    __tablename__ = "registros_estudo"

    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    horas = db.Column(db.Integer, nullable=False)  # quantidade de horas estudadas
    horario = db.Column(db.String(10), nullable=False)  # formato HH:MM

    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
