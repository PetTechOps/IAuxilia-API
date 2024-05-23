import re

def formatar_texto(texto):
    # Definir expressões regulares para cada seção
    regex_patterns = {
        'titulo': r'Título:\s*(.*?)\n\n',
        'sintese': r'Síntese da Situação:\s*(.*?)\n\n',
        'prioridade': r'Prioridade:\s*(.*?)\n\n',
        'localizacao': r'Localização:\s*(.*?)\n\n',
        'recursos': r'Recursos Necessários:(.*?)Ações a Serem Tomadas:',
        'acoes': r'Ações a Serem Tomadas:(.*?)Observações:',
        'observacoes': r'Observações:\s*(.*)'
    }

    # Extrair informações usando regex
    extracoes = {key: re.findall(pattern, texto, re.DOTALL) for key, pattern in regex_patterns.items()}

    # Formatando a saída em HTML
    texto_formatado = ''
    if extracoes['titulo']:
        texto_formatado += f'<h1><strong>{extracoes["titulo"][0]}</strong></h1>'
    if extracoes['sintese']:
        texto_formatado += f'<p><strong>Síntese da Situação:</strong> {extracoes["sintese"][0]}</p><br>'
    if extracoes['prioridade']:
        texto_formatado += f'<p><strong>Prioridade:</strong> {extracoes["prioridade"][0]}</p><br>'
    if extracoes['localizacao']:
        texto_formatado += f'<p><strong>Localização:</strong> {extracoes["localizacao"][0]}</p>'
    if extracoes['recursos']:
        recursos = extracoes['recursos'][0].strip().split('\n')
        texto_formatado += '<h2><strong>Recursos Necessários</strong></h2><ul>'
        for recurso in recursos:
            texto_formatado += f'<li>{recurso}</li>'
        texto_formatado += '</ul>'
    if extracoes['acoes']:
        acoes = extracoes['acoes'][0].strip().split('\n')
        texto_formatado += '<h2><strong>Ações a Serem Tomadas</strong></h2><ol>'
        for acao in acoes:
            texto_formatado += f'{acao}\n'
        texto_formatado += '</ol>'
    if extracoes['observacoes']:
        observacoes = extracoes['observacoes'][0].strip().split('\n')
        texto_formatado += '<h2><strong>Observações</strong></h2><ul>'
        for observacao in observacoes:
            texto_formatado += f'<li>{observacao}</li>'
        texto_formatado += '</ul>'
    
    return texto_formatado

