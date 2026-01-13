import pandas as pd
import os
from core.config import CSV_TICKETS_PATH
from core.config import FOLDER
from core.config import ANO
import yfinance as yf
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def variacao_percentual(ticker, inicio, fim):
    df = yf.download(ticker, start=inicio, end=fim, progress=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    p0 = float(df["Close"].iloc[0])
    p1 = float(df["Close"].iloc[-1])

    return (p1 / p0 - 1) * 100


def graph(df, filter=False):
    
    if filter == True:
        # df = df[(df["desconto_%"] < - 25) & (df["desconto_%"] > -50)].sort_values(by='desconto_%', ascending=True)
        df = df[(df["desconto_%"] < 10) & (df["desconto_%"] > -80)].sort_values(by='desconto_%', ascending=True)
    # print(df[["ticket", "valor_intrinseco", "desconto_%"]])
    
    df_sorted = df.sort_values("desconto_%")

    # 1 ativo com desconto_% > 0 (menor positivo)
    positivo = df_sorted[df_sorted["desconto_%"] > 0].head(2)

    # 2 ativos com desconto_% < 0 (mais próximos de zero)
    negativos = (
        df_sorted[df_sorted["desconto_%"] < 0]
        .sort_values("desconto_%", ascending=False)
        .head(4-len(positivo))
    )   

    # resultado final
    df = pd.concat([positivo, negativos])
    
    # verifica se o arquivo setores.csv existe
    if os.path.exists(f'{CSV_TICKETS_PATH}setores.csv'):
        df_setores = pd.read_csv(
            f'{CSV_TICKETS_PATH}setores.csv',
            sep=';',
            encoding='utf-8')
        
        df["ticker"] = df["ticker"].str.upper()
        df_setores["Ticket"] = df_setores["Ticket"].str.upper()
        
        df_final = df.merge(
        df_setores,
        left_on="ticker",
        right_on="Ticket",
        how="left"
        )
        
        df = df_final[['ticker', 'valor_intrinseco', 'desconto_%', 'preco_inicio',
        'preco_fim', 'variacao_percentual',
        'Subsetor de Atuação', 'Segmento de Atuação']]
        
    else:
        df_final = df.copy()
        df = df.sort_values(by='desconto_%', ascending=False)
    
    # df = df.sort_values(
    # by=["Segmento de Atuação", "desconto_%"],
    # ascending=[True, True]
    # )
    # df = df[:5]
    
    print(df)
    
    media_carteira = df["variacao_%"].mean()
    print(f"Média de variação da carteira: {media_carteira:.2f}%")
    
    inicio = f"{ANO}-01-01"
    fim = f"{ANO}-12-31"


    if FOLDER == "IBOV":
        variacao_indice = variacao_percentual("^BVSP", inicio, fim)
    elif FOLDER == "IDIV":
        variacao_indice = variacao_percentual("DIVD11.SA", inicio, fim)
    else:
        variacao_indice = variacao_percentual("^GSPC", inicio, fim)
    print(f"Desempenho do indice no periodo: {variacao_indice:.2f}%")

    return df["ticker"].tolist()
