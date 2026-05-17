from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = 'salao_secret'

DATABASE_URL = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# TABELAS
# =========================

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(30))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    servico = db.Column(db.String(100))
    data = db.Column(db.String(30))
    horario = db.Column(db.String(20))

# =========================
# ROTAS
# =========================

@app.route('/')
def index():
    return render_template('index.html')

# CLIENTES

@app.route('/clientes')
def clientes():
    lista_clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/adicionar_cliente', methods=['GET', 'POST'])
def adicionar_cliente():

    if request.method == 'POST':

        nome = request.form['nome']
        telefone = request.form['telefone']

        novo = Cliente(
            nome=nome,
            telefone=telefone
        )

        db.session.add(novo)
        db.session.commit()

        return redirect('/clientes')

    return render_template('adicionar_cliente.html')

# AGENDAMENTOS

@app.route('/agendamentos')
def agendamentos():

    lista = Agendamento.query.all()

    return render_template(
        'agendamentos.html',
        agendamentos=lista
    )

@app.route('/adicionar_agendamento', methods=['GET', 'POST'])
def adicionar_agendamento():

    if request.method == 'POST':

        cliente = request.form['cliente']
        servico = request.form['servico']
        data = request.form['data']
        horario = request.form['horario']

        novo = Agendamento(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario
        )

        db.session.add(novo)
        db.session.commit()

        return redirect('/agendamentos')

    return render_template(
        'adicionar_agendamento.html'
    )

# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)