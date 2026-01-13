from valuationForRoe import analyze_ticker
from getBalance import obtem_balanco
from core.config import CSV_TICKETS_PATH
from core.config import FOLDER
from core.config import ANO
from core.config import KE

def executar_automacao(payload: dict):
    ticket = payload["ticket"]
    path = f"{CSV_TICKETS_PATH}{FOLDER}\\"
    
    
    # obtem_balanco(ticket) # Obter balanço
    # return analyze_ticker(path, ticket, ANO, KE) # Valuation
    
    return analyze_ticker(path, ticket, ANO, KE)