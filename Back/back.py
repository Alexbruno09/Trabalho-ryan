from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Config do banco (ajusta conforme teu ambiente)
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "bruno0910",
    "host": "127.0.0.1",
    "port": "5432"
}

# Conectar ao banco
def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Inicializar banco com schema.sql
def init_db():
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(schema)
    conn.commit()
    conn.close()

init_db()

# Rotas -----------------------------

@app.route("/alunos", methods=["POST"])
def criar_aluno():
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("INSERT INTO alunos (nome) VALUES (%s) RETURNING id", (data["nome"],))
    aluno_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return jsonify({"id": aluno_id, "nome": data["nome"]})

@app.route("/alunos", methods=["GET"])
def listar_alunos():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM alunos")
    alunos = cur.fetchall()
    conn.close()
    return jsonify(alunos)

@app.route("/registros", methods=["POST"])
def criar_registro():
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO registros_estudo (aluno_id, materia, horas, data) VALUES (%s, %s, %s, %s) RETURNING id",
        (data["aluno_id"], data["materia"], data["horas"], data["data"])
    )
    registro_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return jsonify({"id": registro_id, **data})

@app.route("/registros/<int:aluno_id>", methods=["GET"])
def listar_registros(aluno_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM registros_estudo WHERE aluno_id = %s", (aluno_id,))
    registros = cur.fetchall()
    conn.close()
    return jsonify(registros)

if __name__ == "__main__":
    app.run(debug=True)
