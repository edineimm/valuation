from core.dataItem import WorkItem
from core.config import CSV_SP500_PATH
from core.config import TOP_COMPANIES
import pandas as pd

def carregar_fila():
        
    df = pd.read_csv(CSV_SP500_PATH,
                    sep=";",
                    decimal = ',',
                    encoding = "utf-8"
                    ) 
    
    df = df[df["Código"].notna()]
    
    # Criação da fila
    
    fila = []
    
    df = df[:TOP_COMPANIES]
    
    for idx, ticket in enumerate (df["Código"].tolist(), start=1):
        fila.append(WorkItem(id=idx,
                             payload = {"ticket": ticket}))
    
    return fila
