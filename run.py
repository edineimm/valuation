from valuationForRoe import analyze_ticker
from core.config import CSV_TICKETS_PATH
from core.config import FOLDER
from core.config import ANO
from core.config import KE

def executar_automacao(payload: dict):
    ticket = payload["ticket"]
    # print(f"Processando ativo {ticket}")
    path = f"{CSV_TICKETS_PATH}{FOLDER}\\"
    return analyze_ticker(path, ticket, ANO, KE)