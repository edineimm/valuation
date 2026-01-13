import pandas as pd
import numpy as np
import os
from core.config import FOLDER
from core.config import CSV_TICKETS_PATH
from webScraping import obtain_financial_indicators
from pathlib import Path

def to_numeric(x):
    if isinstance(x, str):
        x = x.replace('%', '').replace(',', '.').strip()
    return pd.to_numeric(x, errors='coerce')

def preencher_dividendos(df) -> dict:

    arredondar = 2
                
    # Converter apenas P/L e LPA (D.Y NÃO será alterado)
    for row in ['P/L', 'LPA']:
        if row not in df.index:
            raise ValueError(f"Linha obrigatória ausente: {row}")
        df.loc[row] = df.loc[row].apply(to_numeric)

    # Criar D.Y numérico apenas para cálculo (sem alterar df)
    if 'D.Y' not in df.index:
        raise ValueError("Linha obrigatória ausente: D.Y")

    dy_calc = df.loc['D.Y'].apply(to_numeric) / 100

    # Calcular Div
    df.loc['Div'] = df.loc['P/L'] * df.loc['LPA'] * dy_calc

    if arredondar is not None:
        df.loc['Div'] = pd.to_numeric(
            df.loc['Div'], errors='coerce'
        ).round(arredondar)

    return df            



def obtem_balanco(ticket: str): 
       
    print(f"\n=== PROCESSANDO TICKER: {ticket} ===")
    
    path_ticket = Path(f"{CSV_TICKETS_PATH}{FOLDER}\\{ticket}.csv")
    
    indicators = None
    
    if path_ticket.exists():
        # print(f"Arquivo {ticket}.csv já existe. Pulando...")
        return None
    else:
        # obtem os indicadores financeiros
        indicators = obtain_financial_indicators(ticket)

    # obtem os dividendos e preenche o dataframe  
    
    if indicators is None or indicators.empty:
        print(f"Nenhum indicador financeiro encontrado para o ticker {ticket}. Pulando...")
    else:
        indicators = preencher_dividendos(indicators)
        indicators.to_csv(f'{CSV_TICKETS_PATH}{FOLDER}\\{ticket}.csv', sep=';', encoding='utf-8')