import os
from flask import Flask, request, render_template, redirect, session, url_for
from dotenv import load_dotenv

from models import db, Usuario, Cliente, Agendamento

load_dotenv()

app = Flask(__name__)
app.secret_key = "chave_super_secreta_salao_2026"

# ================= BANCO =================
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {"sslmode": "require"}
}

db.init_app(app)

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/plano")
def plano():
    return render_template("plano.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        senha = request.form["senha"].strip()

        user = Usuario.query.filter_by(
            email=email,
            senha=senha
        ).first()

        if user:

            session["user_id"] = user.id
            session["user_email"] = user.email

            return redirect(url_for("clientes"))

        return "Login inválido"

    return render_template("login.html")


# ================= CADASTRO =================
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        email = request.form["email"].strip()
        senha = request.form["senha"].strip()

        if not email or not senha:
            return "Preencha todos os campos"

        existe = Usuario.query.filter_by(
            email=email
        ).first()

        if existe:
            return "Usuário já existe"

        novo = Usuario(
            email=email,
            senha=senha
        )

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("cadastro.html")


# ================= USUÁRIO TESTE =================
@app.route("/criar-user")
def criar_user():

    user = Usuario(
        email="admin@admin.com",
        senha="123"
    )

    db.session.add(user)
    db.session.commit()

    return "Usuário criado com sucesso!"


# ================= DEBUG USERS =================
@app.route("/users")
def users():
    return str(Usuario.query.all())


# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ================= CLIENTES =================
@app.route("/clientes")
def clientes():

    if "user_id" not in session:
        return redirect(url_for("login"))

    clientes = Cliente.query.filter_by(
        usuario_id=session["user_id"]
    ).all()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# ================= EXCLUIR CLIENTE =================
@app.route("/excluir_cliente/<int:id>")
def excluir_cliente(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cliente = Cliente.query.get(id)

    if cliente:

        agendamentos = Agendamento.query.filter_by(
            cliente_id=id
        ).all()

        for a in agendamentos:
            db.session.delete(a)

        db.session.delete(cliente)

        db.session.commit()

    return redirect(url_for("clientes"))


# ================= ADICIONAR CLIENTE =================
@app.route("/adicionar_cliente", methods=["GET", "POST"])
def adicionar_cliente():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        novo = Cliente(
            nome=request.form["nome"],
            telefone=request.form["telefone"],
            usuario_id=session["user_id"]
        )

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("clientes"))

    return render_template("adicionar_cliente.html")


# ================= AGENDAMENTOS =================


# ================= EXCLUIR AGENDAMENTO =================


    # ================= AGENDAMENTOS =================
@app.route("/agendamentos")
def agendamentos():

    if "user_id" not in session:
        return redirect(url_for("login"))

    agendamentos = Agendamento.query.all()

    return render_template(
        "agendamentos.html",
        agendamentos=agendamentos
    )


# ================= EXCLUIR AGENDAMENTO =================
@app.route("/excluir_agendamento/<int:id>")
def excluir_agendamento(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    agendamento = Agendamento.query.get(id)

    if agendamento:

        db.session.delete(agendamento)
        db.session.commit()

    return redirect(url_for("agendamentos"))


# ================= ADICIONAR AGENDAMENTO =================
@app.route("/adicionar_agendamento", methods=["GET", "POST"])
def adicionar_agendamento():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        novo = Agendamento(
            cliente_id=request.form["cliente_id"],
            servico=request.form["servico"],
            data=request.form["data"],
            hora=request.form["hora"]
        )

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("agendamentos"))

    clientes = Cliente.query.filter_by(
        usuario_id=session["user_id"]
    ).all()

    return render_template(
        "adicionar_agendamento.html",
        clientes=clientes
    )


# ================= INIT =================
@app.route("/init")
def init():

    with app.app_context():
        db.create_all()

    return "Banco criado"


# ================= RESETAR =================
@app.route("/resetar")
def resetar():

    with app.app_context():

        db.drop_all()

        db.create_all()

    return "Banco resetado!"


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)