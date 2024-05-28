from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome = db.Column(db.String(50))
  cep = db.Column(db.String(9))
  prompt = db.Column(db.String)
  saida = db.Column(db.String)
  prioridade = db.Column(db.String(1))

  def __init__(self, nome, cep, prompt, saida, prioridade):
    self.nome = nome
    self.cep = cep
    self.prompt = prompt
    self.saida = saida
    self.prioridade = prioridade