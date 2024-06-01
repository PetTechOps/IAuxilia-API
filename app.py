# pip install flask-sqlalchemy flask-migrate google-generativeai python-dotenv
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from sqlalchemy import desc
from model import db, Usuario
from gemini import Gemini
from cep import CEPService
from formatar import formatar_texto
import re

# Criando um app Flask e Configurando o SQL_Alchemy para usar o banco SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

# Utilizando migrate para o versionamento de Banco de Dados
db.init_app(app)
migrate = Migrate(app, db)

# ROTA DE CADASTRO
@app.get('/')
@app.get('/cadastro')
def index_get():
  return render_template('index.html')


# CREATE
@app.post('/prompt')
def index_post():
  gemini_instance = Gemini.get_instance() # Criando uma Instância da classe Gemini
  chat = gemini_instance.start_chat() # Criando o chat que faz conexão com a API do Gemini
  
  nome = request.form.get('nome')  # Recebendo o nome na Entrada
  cep = request.form.get('cep') # Recebendo o CEP na Entrada
  prompt = request.form.get('prompt') # Recebendo o Prompt/Relato na Entrada
  
  if cep: # Verificando se o cep foi preenchido
    if not CEPService.is_valid_cep(cep):
      return render_template('erro.html', msg='Formato de CEP inválido!')
    info_cep = CEPService.obter_info_cep(cep) # Consultando as informações do CEP
    if info_cep: prompt = f'{prompt}, {info_cep.values()}' # Preparando a mensagem que vai para o prompt
    else: return render_template('erro.html', msg='CEP não encontrado!')  # Retornar um erro caso o CEP seja no formato inválido ou se não foi encontrado
  
  # Se não tiver informações do CEP, enviaremos apenas o relato
  response = chat.send_message(prompt) # Envio da mensagem para o Gemini
  saida = response.text.replace('*','') # Removendo todas as ocorrências de * (Utilizado para deixar em negrito)
  prioridade_txt = re.search(r'Prioridade:\s*(.*)', saida) # Regex para filtrar a primeira ocorrência de Prioridade
  if not prioridade_txt:
     return render_template('erro.html', msg='Desculpe, mas o relato inserido não está de acordo com o objetivo de resgate.')
  prioridade_num = re.findall(r'\d', prioridade_txt.group())[0] # Regex para filtrar apenas o número da ocorrência

  usuario = Usuario(nome, cep, prompt, saida, prioridade_num) # Criação de uma instância de Usuario 
  db.session.add(usuario) # Adicionando o usuario criado no Banco SQLite 
  db.session.commit() # Confirmando o comando 
  
  saida = formatar_texto(saida) # Função que formata a saída do Gemini para ser exibida de uma forma mais agradável
  return render_template('saida.html', usuario=usuario, saida=saida)  # Exibindo a tela com a saída


# READ
@app.get('/resgates')
def resgates_get():
  usuarios = Usuario.query.order_by(desc(Usuario.prioridade)).all()
  return render_template('resgates.html', usuarios=usuarios)


# ROTA DE PERFIL
@app.get('/perfil/<int:id>')
def exibir_perfil(id):
   usuario = Usuario.query.get(id)
   return render_template('atualizar.html', usuario=usuario)


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


# ERROR
@app.errorhandler(404)
def page_not_found(e):
    return render_template('erro.html', msg='Página não encontrada!')

if __name__ == '__main__':
  app.run(debug=True)