from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

class Gemini:
    _instance = None

    def __init__(self):
        if not self.__class__._instance:
            self.GOOGLE_API_KEY = os.getenv("SECRET_KEY")
            if not self.GOOGLE_API_KEY:
                raise ValueError("A chave da API do Google não foi encontrada no .env")
            self.configure_gemini()
            self.__class__._instance = self
        else:
            print("Usando instância existente de Gemini")


    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Gemini()
        return cls._instance


    #API Gemini configurada
    def configure_gemini(self):
        genai.configure(api_key=self.GOOGLE_API_KEY)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        self.system_instruction = (
            "Você é um agente especialista em socorros em uma ONG e dado um determinado relato, "
            "você analise qual o melhor caminho ou coisas necessárias para resolver essa situação. "
            "Passe instruções para uma equipe operacional, como uma espécie de chamado, para resolver esse problema "
            "julgue um nível de prioridade de 1 a 5 e forneça o bairro."
        )
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=self.generation_config,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings,
        )


    def start_chat(self):
        # Iniciando chat com o modelo Gemini
        chat = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": ["Dado uma entrada, forneça uma resposta seguindo o exemplo da saída. Para entradas fora desse contexto, retorne 'Desculpe, mas o tipo de entrada inserido não está de acordo com o solicitado', lembrando que todos os títulos precisam estar em <strong> para que a exibição fique melhor. Exemplo de chamado para Prioridade nível 5 Entrada: No bairro que estou Moinhos de Vento, a água da enchente ultrapassou 5 metros de altura, não temos alimentos e nem lugar para estocar as coisas. Uma canoa não consegue chegar aqui por conta dos destroços ao redor do caminho, tem cerca de 30 pessoas aqui comigo, estamos em cima de um telhado e existem 3 crianças feridas no local. Saída: <strong>Título:</strong> Resgate Urgente: Grupo Isolado em Telhado após Inundações em Porto Alegre <strong>Síntese da Situação:</strong> Grupo de 30 pessoas e 3 crianças feridas isoladas em um telhado devido à inundação, sem acesso a alimentos e com obstáculos na água impedindo o resgate por barcos. <strong>Prioridade:</strong> Nível 5 - Emergência Máxima. <strong>Localização:</strong> Moinhos de Vento, Porto Alegre, Rio Grande do Sul. <strong>Recursos Necessários:</strong> * Helicóptero para resgate aéreo. * Equipe de resgate especializada em salvamento aquático e em altura. * Equipamentos de salvamento: Cordas, macas, coletes salva-vidas, kits de primeiros socorros. * Suprimentos essenciais: Alimentos, água potável, cobertores e roupas secas. <strong>Ações a Serem Tomadas:</strong> 1. Confirmar a localização exata do grupo. 2. Deslocar o helicóptero com a equipe de resgate para o local. 3. Avaliar a situação e as condições do local. 4. Realizar o resgate utilizando técnicas adequadas. 5. Prestar primeiros socorros, se necessário. 6. Transportar as vítimas para um local seguro. 7. Fornecer alimentos, água, cobertores e roupas secas. 8. Verificar a disponibilidade de recursos na região. 9. Comunicar a situação ao centro de operações de emergência local. <strong>Observações:</strong> Manter contato constante com o grupo isolado para obter informações atualizadas. Priorizar a segurança da equipe de resgate em condições adversas. Coordenar esforços com outras equipes de emergência na região. -------------------------------------------------------------------------------------------------------------------------- Exemplo de chamado para Prioridade nível 4 Entrada: A minha casa está cheia de água, eu perdi tudo, estou ilhada e não consigo sair para comprar comida, os meus filhos estão chorando de fome, não temos nem roupa seca e nem lugar para dormir a água tomou tudo, bairro Anchieta Saída: <strong>Título:</strong> Resgate Urgente: Família Ilhada por Inundações em Porto Alegre <strong>Síntese da Situação:</strong> Família ilhada em casa inundada no bairro Anchieta, sem acesso a alimentos, roupas secas ou local seguro para dormir. Crianças presentes e necessitando de assistência. <strong>Prioridade:</strong> Nível 4 - Emergência Alta. <strong>Localização:</strong> Anchieta, Porto Alegre, Rio Grande do Sul. <strong>Recursos Necessários:</strong> * Equipe de resgate com bote inflável ou veículo anfíbio capaz de navegar em águas rasas e superar obstáculos. * Suprimentos essenciais: Alimentos, água potável, cobertores, roupas secas, kits de higiene. * Acomodação temporária em abrigo ou alojamento. <strong>Ações a Serem Tomadas:</strong> 1. Confirmar a localização exata da família e avaliar a situação da inundação no local. 2. Deslocar a equipe de resgate com bote ou veículo anfíbio para o local. 3. Realizar o resgate da família, garantindo a segurança de todos. 4. Prestar apoio emocional e verificar a necessidade de atendimento médico. 5. Fornecer alimentos, água, cobertores, roupas secas e kits de higiene. 6. Transportar a família para um abrigo ou alojamento temporário. 7. Registrar a situação da família e oferecer suporte para acesso a programas de assistência social. <strong>Observações:</strong> Manter contato constante com a família para obter informações atualizadas. Avaliar a possibilidade de danos estruturais na residência antes do retorno da família. Coordenar esforços com outras equipes de emergência na região. Investigar a necessidade de apoio psicológico para a família. -------------------------------------------------------------------------------------------------------------------------- Exemplo de chamado para Prioridade nível 3 Entrada: No bairro [Restinga], a água da chuva invadiu minha casa, estragando móveis e alimentos. A água já baixou, mas a rua ainda está alagada, com muita lama e lixo. Preciso de ajuda para limpar minha casa e remover os entulhos. Saída: <strong>Título:</strong> Solicitação de Apoio: Limpeza e Remoção de Entulho após Inundação em Porto Alegre <strong>Síntese da Situação:</strong> Morador do bairro Restinga necessita de ajuda para limpar a residência e remover entulho após inundação. A água baixou, mas a rua ainda está alagada, com muita lama e lixo. <strong>Prioridade:</strong> Nível 3 - Prioridade Média. <strong>Localização:</strong> Restinga, Porto Alegre, Rio Grande do Sul. <strong>Recursos Necessários:</strong> * Equipe de apoio com equipamentos de limpeza: Pá, vassoura, rodo, baldes, botas de borracha. * Caminhão para remoção de entulho e lixo. * Materiais de limpeza: Água sanitária, desinfetante, detergente. <strong>Ações a Serem Tomadas:</strong> 1. Confirmar a localização exata do morador e avaliar a situação da residência. 2. Deslocar a equipe de apoio com os equipamentos de limpeza para o local. 3. Auxiliar na limpeza da residência, removendo lama, lixo e entulho. 4. Desinfetar a residência para prevenir doenças. 5. Remover o entulho e lixo com o caminhão, encaminhando para local apropriado. 6. Registrar a situação do morador e oferecer informações sobre programas de assistência social, caso necessite. <strong>Observações:</strong> Verificar a necessidade de outros tipos de apoio, como alimentos, água potável ou roupas. Coordenar esforços com outras equipes de apoio na região. -------------------------------------------------------------------------------------------------------------------------- Exemplo de chamado para Prioridade nível 2 Entrada: Após a tempestade, a rua [Tristeza] está bloqueada por árvores caídas. Não consigo sair de casa e preciso ir trabalhar. Saída: <strong>Título:</strong> Remoção de Obstáculos: Rua Bloqueada por Árvores Caídas em Porto Alegre <strong>Síntese da Situação:</strong> Rua Tristeza bloqueada por árvores caídas após tempestade, impedindo a passagem de veículos e pedestres. <strong>Prioridade:</strong> Nível 2 - Prioridade Moderada. <strong>Localização:</strong> Tristeza, Porto Alegre, Rio Grande do Sul. <strong>Recursos Necessários:</strong> * Equipe de apoio com motosserras e equipamentos de segurança. * Caminhão para remoção dos galhos e troncos. <strong>Ações a Serem Tomadas:</strong> 1. Confirmar a localização exata da rua bloqueada e avaliar a situação. 2. Deslocar a equipe de apoio com os equipamentos necessários para o local. 3. Remover as árvores caídas com segurança, utilizando as motosserras. 4. Cortar os galhos e troncos em tamanhos adequados para transporte. 5. Remover os resíduos com o caminhão, encaminhando para local apropriado. 6. Liberar a rua para o tráfego de veículos e pedestres. <strong>Observações:</strong> Verificar a existência de fios elétricos na área antes de iniciar os trabalhos. Garantir a segurança da equipe de apoio e dos moradores da região. Coordenar esforços com outras equipes de apoio na região, caso necessário. -------------------------------------------------------------------------------------------------------------------------- Exemplo de chamado para Prioridade nível 1 Entrada: No bairro [Partenon], a chuva forte causou alguns pontos de alagamento na rua, e o bueiro da esquina está entupido. Saída: <strong>Título:</strong> Manutenção Preventiva: Alagamento e Bueiro Entupido em Porto Alegre <strong>Síntese da Situação:</strong> Pontos de alagamento no bairro Partenon devido à chuva forte, com bueiro entupido na esquina. <strong>Prioridade:</strong> Nível 1 - Baixa Prioridade. <strong>Localização:</strong> Partenon, Porto Alegre, Rio Grande do Sul. <strong>Recursos Necessários:</strong> * Equipe de manutenção com ferramentas para desobstrução de bueiros. * Equipamentos de segurança: Luvas, botas, cones de sinalização. <strong>Ações a Serem Tomadas:</strong> 1. Confirmar a localização exata do bueiro entupido e avaliar a situação do alagamento. 2. Deslocar a equipe de manutenção com os equipamentos necessários para o local. 3. Sinalizar a área para garantir a segurança da equipe e dos pedestres. 4. Desobstruir o bueiro utilizando as ferramentas adequadas.\n5. Remover o lixo e entulho do local, garantindo o escoamento da água.\n\nObservações:\nVerificar a necessidade de outros serviços de manutenção na região.\nMonitorar a situação do alagamento após a desobstrução do bueiro.\nOrientar os moradores sobre a importância de não jogar lixo nas ruas."]
            },
        ])
        return chat
