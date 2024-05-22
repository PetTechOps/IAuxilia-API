import requests
def obter_info_cep(cep):
  response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
  if response.status_code == 200:
      data = response.json()
      endereco = {
          "logradouro": data.get("logradouro", ""),
          "complemento": data.get("complemento", ""),
          "bairro": data.get("bairro", ""),
          "localidade": data.get("localidade", ""),
          "uf": data.get("uf", "")
      }
      return endereco
  else:
      return None