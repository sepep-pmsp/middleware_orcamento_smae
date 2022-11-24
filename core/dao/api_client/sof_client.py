from functools import partial
from .abstract_client import Client


class ParserDotacao:

    def validate_dotacao(self, dotacao_split:list)->None:

        if len(dotacao_split)!=9:
            raise ValueError(f'Dotacao fora do padrão: {".".join(dotacao_split)}')

        caracteres = ''.join(dotacao_split)

        if len(caracteres)!=27:
            raise ValueError(f'Dotacao fora do padrão: {".".join(dotacao_split)}')

    def parse_dotacao(self, dotacao:str)->dict:

        dotacao = dotacao.split('.')
        self.validate_dotacao(dotacao)

        parsed = {
            'codOrgao' : dotacao[0],
            'codUnidade' : dotacao[1],
            'codFuncao' : dotacao[2],
            'codSubFuncao' : dotacao[3],
            'codPrograma' : dotacao[4],
            'codProjetoAtividade' : dotacao[5]+dotacao[6],
            'codCategoria' : dotacao[7][1],
            'codGrupo' : dotacao[7][1],
            'codModalidade' : dotacao[7][2:4],
            'codElemento' : dotacao[7][4:6],
            #nao vou pesquisar por subelemento porque o pessoal não preenche
            #'codSubElemento' : dotacao[7][6:8],
            'codFonteRecurso' : dotacao[8]
        }

        return parsed

    def __call__(self, dotacao:str)->dict:

        return self.parse_dotacao(dotacao)

class SofClient:

    host = 'gatewayapi.prodam.sp.gov.br:443'
    base_path = '/financas/orcamento/sof/'
    version = 'v3.0.1'

    def __init__(self, auth_token:str)->None:
    
        self.base_url = self.__build_base_url()
        self.auth_token = auth_token

        self.get = self.__authorize_get()

        self.parse_dotacao = ParserDotacao()

    def __build_base_url(self):

        return f'https://{self.host}{self.base_path}{self.version}/'

    def __build_headers(self):

        return {"Authorization" : f"Bearer {self.auth_token}",
                "Accept": "application/json"}

    def __authorize_get(self):

        client = Client(self.base_url)
        headers = self.__build_headers()
        get = partial(client.get, headers=headers)

        return get

    def empenhos_processo(self, ano:int, mes:int, proc:int)->dict:

        endpoint = 'empenhos'
        params = {
            'anoEmpenho' : ano,
            'mesEmpenho' : mes,
            'numProcesso' : proc}

        return self.get(endpoint, **params)


    def empenhos_nota_empenho(self, ano:int, mes:int, cod_nota:int)->dict:

        endpoint = 'empenhos'
        params = {
            'anoEmpenho' : ano,
            'mesEmpenho' : mes,
            'codEmpenho' : cod_nota}

        return self.get(endpoint, **params)


    def empenhos_dotacao(self, ano:int, mes:int, dotacao:str)->dict:

        endpoint = 'empenhos'

        dotacao = self.parse_dotacao(dotacao)
        dotacao['anoEmpenho'] = ano
        dotacao['mesEmpenho'] = mes
        

        return self.get(endpoint, **dotacao)

    def __check_params(self, dotacao:str=None, processo:str=None, 
                nota_empenho:str=None)->None:

        params = (dotacao, processo, nota_empenho)
        checksum= sum(p for p in params if not p is None)

        if checksum==0:
            raise ValueError('Either dotacao, processo or nota_empenho must be defined.')
        if checksum>1:
            raise ValueError('Only one of dotacao, processo or nota_empenho must be defined.')

    def __call__(self, ano:int, mes:int, dotacao:str=None, 
        processo:int=None, nota_empenho: int=None)->dict:

        self.__check_params(dotacao, processo, nota_empenho)

        if dotacao:
            return self.empenhos_dotacao(ano, mes, dotacao)
        if processo:
            return self.empenhos_processo(ano, mes, processo)
        if nota_empenho:
            return self.empenhos_nota_empenho(ano, mes, nota_empenho)
        


    