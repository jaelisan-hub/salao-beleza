from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(50))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )


class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("cliente.id")
    )

    servico = db.Column(db.String(100))
    data = db.Column(db.String(20))
    hora = db.Column(db.String(20))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )