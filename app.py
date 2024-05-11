from flask import Flask, render_template, request
from gemini import gemini_connect
from model import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gemini.db'
db.init_app(app)

@app.get('/')
def index_get():
  text = "IAuxilia Gemini"
  return render_template('index.html',text=text)

@app.post('/resposta')
def index_post():
  conversa = gemini_connect()
  nome = request.form.get('nome')
  relato = request.form.get('relato')
  response = conversa.send_message(relato)
  resposta = response.text.replace('*','')
  usuario = Usuario(nome,relato,resposta)
  db.session.add(usuario)
  db.session.commit()
  return render_template('resposta.html',resposta=resposta)

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
