import re
def formatar_texto(texto):
    # Definir expressões regulares para cada seção
    regex_patterns = {
        'titulo': r'Título:\s*(.*)',
        'sintese': r'Síntese da Situação:\s*(.*)',
        'prioridade': r'Prioridade:\s*(.*)',
        'localizacao': r'Localização:\s*(.*)',
        'recursos': r'Recursos Necessários:\s*(.*?)(?=Ações a Serem Tomadas:|Observações:|$)',
        'acoes': r'Ações a Serem Tomadas:\s*(.*?)(?=Observações:|$)',
        'observacoes': r'Observações:\s*(.*)'
    }

    # Extrair informações usando regex
    extracoes = {key: re.findall(pattern, texto, re.DOTALL) for key, pattern in regex_patterns.items()}

    # Formatando a saída em HTML
    texto_formatado = ''
    if extracoes['titulo']:
        texto_formatado += f'<h1>{extracoes["titulo"][0]}</h1>'
    if extracoes['sintese']:
        texto_formatado += f'<p><strong>Síntese da Situação:</strong> {extracoes["sintese"][0]}</p>'
    if extracoes['prioridade']:
        texto_formatado += f'<p><strong>Prioridade:</strong> {extracoes["prioridade"][0]}</p>'
    if extracoes['localizacao']:
        texto_formatado += f'<p><strong>Localização:</strong> {extracoes["localizacao"][0]}</p>'
    if extracoes['recursos']:
        recursos = extracoes['recursos'][0].strip().split('\n')
        texto_formatado += '<h2>Recursos Necessários</h2><ul>'
        for recurso in recursos:
            texto_formatado += f'<li>{recurso}</li>'
        texto_formatado += '</ul>'
    if extracoes['acoes']:
        acoes = extracoes['acoes'][0].strip().split('\n')
        texto_formatado += '<h2>Ações a Serem Tomadas</h2><ol>'
        for acao in acoes:
            texto_formatado += f'<li>{acao}</li>'
        texto_formatado += '</ol>'
    if extracoes['observacoes']:
        texto_formatado += f'<h2>Observações</h2><p>{extracoes["observacoes"][0]}</p>'
    
    return texto_formatado