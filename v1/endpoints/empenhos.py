from fastapi import APIRouter, Depends
from typing import List

from core.dao import DaoEmpenhos
from core.schemas import empenhos as schm_empenho
from config import SOF_API_TOKEN

app = APIRouter()


def get_dao():

    dao = DaoEmpenhos(auth_token=SOF_API_TOKEN)
    
    return dao

@app.post("/nota_empenho", response_model=List[schm_empenho.Empenhos], tags=['Empenhos'])
def empenho_nota(nota_empenho:schm_empenho.NotaEmpenho, dao: DaoEmpenhos = Depends(get_dao)):

    ano = nota_empenho.ano
    mes = nota_empenho.mes
    nota_empenho = nota_empenho.nota_empenho

    result = dao.nota_empenho(ano=ano, mes=mes, nota_empenho=nota_empenho)
    return result

@app.post("/processo", response_model=List[schm_empenho.Empenhos], tags=['Empenhos'])
def empenho_proc(processo:schm_empenho.Processo, dao: DaoEmpenhos = Depends(get_dao)):

    ano = processo.ano
    mes = processo.mes
    processo = processo.processo

    result = dao.processo(ano=ano, mes=mes, processo=processo)
    return result

@app.post("/dotacao", response_model=List[schm_empenho.Empenhos], tags=['Empenhos'])
def empenho_dotacao(dotacao:schm_empenho.Dotacao, dao: DaoEmpenhos = Depends(get_dao)):

    ano = dotacao.ano
    mes = dotacao.mes
    dotacao = dotacao.dotacao

    result = dao.processo(ano=ano, mes=mes, dotacao=dotacao)
    return result