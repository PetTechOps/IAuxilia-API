from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
  __tablename__ = 'Usuario'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome = db.Column(db.String(50))
  relato = db.Column(db.String)
  resposta = db.Column(db.String)

  def __init__(self, nome, relato, resposta):
    self.nome = nome
    self.relato = relato
    self.resposta = resposta



  


