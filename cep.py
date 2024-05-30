import requests
import re

class CEPService:
    BASE_URL = 'https://viacep.com.br/ws'

    @staticmethod
    def obter_info_cep(cep):
        if not CEPService.is_valid_cep(cep):
            return None
        
        url = f'{CEPService.BASE_URL}/{cep}/json/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'erro' in data:
                return None
            endereco = {
                "logradouro": data.get("logradouro", ""),
                "complemento": data.get("complemento", ""),
                "bairro": data.get("bairro", ""),
                "localidade": data.get("localidade", ""),
                "uf": data.get("uf", "")
            }
            return endereco
        return None

    @staticmethod
    def is_valid_cep(cep):
        return re.fullmatch(r'\d{8}|\d{5}-\d{3}', cep) is not None
