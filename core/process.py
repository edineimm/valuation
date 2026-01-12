import time
import traceback
import pandas as pd
from core.dataItem import WorkItem, Status
from datetime import datetime
from run import executar_automacao
from core.config import MAX_RETRY
from core.config import FOLDER

def processar_item(item: WorkItem) -> WorkItem:
    item.inicio = datetime.now()

    try:
        item.tentativa += 1

        # =========================
        # LÓGICA DE NEGÓCIO
        # =========================
        
        # armazena dados de retorno do item
        dados = executar_automacao(item.payload)
        item.resultado = dados

        item.status = Status.COMPLETO

    except Exception as e:
        item.erro = traceback.format_exc()

        if item.tentativa < MAX_RETRY:
            return processar_item(item)  # retry
        else:
            item.status = Status.EXCECAO

    finally:
        item.fim = datetime.now()

    return item

def consolidar_dataframe(resultados: list[WorkItem]) -> pd.DataFrame:
    linhas = []

    for item in resultados:
        # base = {
        #     "key_item": item.id,
        #     "status": item.status.value,
        #     "tentativas": item.tentativa,
        #     "erro": item.erro.splitlines()[-1] if item.erro else ""
        # }

        # # merge seguro dos dados do item
        # base.update(item.resultado)

        # linhas.append(base)
        
        linhas.append(item.resultado)

    return pd.DataFrame(linhas)
