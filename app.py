from flask import Flask, render_template, request, redirect
from model import db, User
from gemini import Gemini_Connect
from cep import obter_info_cep
from formatar import formatar_texto
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

db.init_app(app)

@app.route('/limpar_bd', methods=['POST'])
def limpar_banco_de_dados():
    with app.app_context():
        db.drop_all()
    return 'Banco de dados limpo com sucesso!'

@app.delete('/deletar/<id>')
def deletar(id):
   usuario = User.query.filter_by(id = id).first()
   db.session.delete(usuario)
   db.session.commit()
   return redirect('/resgates')

@app.get('/')
@app.get('/cadastro')
def index_get():
  return render_template('index.html')

@app.get('/resgates')
def resgates_get():
  usuarios = User.query.all()
  return render_template('resgates.html', usuarios = usuarios)

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
  usuario = User(nome, cep, prompt, saida, prioridade) # Criação de uma instância de User 
  db.session.add(usuario) # Adicionando o usuario criado no Banco SQLite 
  db.session.commit() # Confirma o comando 
  saida = formatar_texto(saida)
  return render_template('saida.html', usuario=usuario, saida=saida)  # Exibe tela com a saída


if __name__ == '__main__':
  with app.app_context():
      db.create_all()
  app.run(debug=True)

