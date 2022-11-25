from typing import List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, validator, root_validator

from ..utils.utils_dotacao import validacao_dotacao


class BuscaEmpenho(BaseModel):

    ano : int
    mes : int

    @root_validator
    def check_future_time(cls, values):

        ano = values.get('ano')
        mes = values.get('mes')

        req_dt = datetime(year=ano, month=mes, day=1)

        if datetime.today()<req_dt:
            raise ValueError(f'Data pesquisada {mes}/{ano} no futuro.')

        return values

class NotaEmpenho(BuscaEmpenho):

    nota_empenho: str

    @validator('nota_empenho', pre=True, always=True)
    def format_nota(cls, v):

        valor_original = v
        formatado = v.split('/')[0]
        formatado = formatado.strip()

        if len(formatado)!=5:
            raise ValueError(f'Nota de empenho {valor_original} fora do padrão.')

        try:
            return int(formatado)
        except ValueError:
            raise ValueError(f'Nota de empenho {valor_original} fora do padrão.')


class Processo(BuscaEmpenho):

    processo: str
    
    @validator('processo', pre=True, always=True)
    def format_proc(cls, v):

        valor_original = v
        formatado = v.replace('.', '').replace('/', '')
        formatado = formatado.strip()

        if len(formatado)!=16: 
            raise ValueError(f'Processo {valor_original} fora do padrão.')
        
        try:
            return int(formatado)
        except ValueError:
            raise ValueError(f'Processo {valor_original} fora do padrão.')


class Dotacao(BuscaEmpenho):

    dotacao: str

    @validator('dotacao', pre=True, always=True)
    def format_dotacao(cls, v):

        validacao_dotacao(v)

        return v
