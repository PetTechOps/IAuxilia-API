from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from model import db, Usuario
from gemini import Gemini_Connect
from cep import obter_info_cep
from formatar import formatar_texto
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

db.init_app(app)
migrate = Migrate(app, db)

@app.get('/')
@app.get('/cadastro')
def index_get():
  return render_template('index.html')


# CREATE
@app.post('/prompt')
def index_post():
  chat = Gemini_Connect() # Criando o chat, que faz conexão com a API do Gemini
  nome = request.form.get('nome')  # Entrada
  cep = request.form.get('cep') # Entrada
  prompt = request.form.get('prompt') # Entrada
  info_cep = obter_info_cep(cep) # Realiza a requisição do CEP
  if not cep:  # Verificar se o campo do CEP não está vazio
      info_cep = ""  # Definir o endereço como uma string vazia
  else:
      info_cep = obter_info_cep(cep)
      if not info_cep:
        return render_template('erro.html')
  response = chat.send_message(f'{prompt},{info_cep.values()}') # Envio da mensagem para o Gemini
  saida = response.text.replace('*','') # Saída
  prioridade = re.findall(r'Prioridade:\s*(.*)', saida)[0] # Regex para filtrar a primeira ocorrência de Prioridade
  usuario = Usuario(nome, cep, prompt, saida, prioridade.replace("</strong>", "")) # Criação de uma instância de Usuario 
  db.session.add(usuario) # Adicionando o usuario criado no Banco SQLite 
  db.session.commit() # Confirma o comando 
  saida = formatar_texto(saida)
  return render_template('saida.html', usuario=usuario, saida=saida)  # Exibe tela com a saída


# READ
@app.get('/resgates')
def resgates_get():
  usuarios = Usuario.query.all()
  return render_template('resgates.html', usuarios = usuarios)


@app.get('/perfil/<int:id>')
def exibir_perfil(id):
   usuario = Usuario.query.get(id)
   return render_template('atualizar.html', usuario = usuario)


# UPDATE
@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar_usuario(id):
   usuario = Usuario.query.get(id)
   usuario.nome = request.form.get('nome')
   usuario.cep = request.form.get('cep')
   usuario.prompt = request.form.get('prompt')
   db.session.commit()
   return redirect('/resgates')


# DELETE
@app.route('/deletar/<int:id>', methods=['GET', 'DELETE'])
def deletar(id):
  usuario = Usuario.query.get(id)
  db.session.delete(usuario)
  db.session.commit()
  return redirect('/resgates')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('erro.html')

if __name__ == '__main__':
  # with app.app_context():
  #     db.create_all()
  app.run(debug=True)