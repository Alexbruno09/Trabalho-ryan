from flask import Flask, render_template, request, redirect, url_for
from models import db, Aluno, Registro
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diario.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    alunos = Aluno.query.all()
    return render_template("index.html", alunos=alunos)

@app.route("/aluno/novo", methods=["GET", "POST"])
def novo_aluno():
    if request.method == "POST":
        nome = request.form["nome"]
        novo = Aluno(nome=nome)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("aluno.html")

@app.route("/aluno/<int:aluno_id>")
def ver_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    return render_template("registro_form.html", aluno=aluno)

@app.route("/aluno/<int:aluno_id>/registro", methods=["POST"])
def novo_registro(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    materia = request.form["materia"]
    conteudo = request.form["conteudo"]
    horas = int(request.form["horas"])
    horario = request.form["horario"]

    registro = Registro(materia=materia, conteudo=conteudo, horas=horas, horario=horario, aluno=aluno)
    db.session.add(registro)
    db.session.commit()
    return redirect(url_for("ver_aluno", aluno_id=aluno.id))

@app.route("/registro/<int:registro_id>/delete")
def delete_registro(registro_id):
    registro = Registro.query.get_or_404(registro_id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for("ver_aluno", aluno_id=registro.aluno_id))

if __name__ == "__main__":
    app.run(debug=True)
