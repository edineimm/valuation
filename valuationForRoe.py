import numpy as np
import pandas as pd
import yfinance as yf
from typing import Dict
from core.config import FOLDER

# =========================
# CONFIGURAÇÕES DE NEGÓCIO
# =========================
MAX_ROE = 0.35
MAX_GROWTH = 0.25
MAX_PAYOUT = 0.80


# =========================
# UTILIDADES
# =========================
def to_float(value) -> float:
    """Converte strings financeiras em float."""
    if pd.isna(value) or value in {"-%", "-", "%", ""}:
        return np.nan

    if isinstance(value, str):
        value = (
            value.strip()
            .replace(".", "")
            .replace(",", ".")
            .replace("%", "")
        )

    try:
        return float(value)
    except ValueError:
        return np.nan


def cagr(series: pd.Series, years: int = 3) -> float:
    """
    CAGR considerando o valor atual + N anos anteriores.
    """
    values = series.dropna().iloc[: years + 1]

    if len(values) < years + 1:
        return np.nan

    v_final = values.iloc[0]
    v_inicial = values.iloc[-1]

    if v_inicial <= 0 or v_final <= 0:
        return np.nan

    return (v_final / v_inicial) ** (1 / years) - 1


# =========================
# DATA LOADER
# =========================
def load_financial_dataframe(file_path: str, ano: int) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=";", encoding="utf-8", index_col=0)

    # Remove colunas futuras
    future_years = [str(y) for y in range(ano, 2026)]
    df = df.drop(columns=future_years, errors="ignore")

    # Limpeza
    df = df.apply(lambda col: col.map(to_float))

    return df

# =========================
# VALUATION ENGINE
# =========================
def valuation_via_roe(
    df: pd.DataFrame,
    ke: float,
    g_perpetuidade: float,
    anos_crescimento: int
) -> float:
    # ---------- LPA ----------
    if "LPA" not in df.index:
        raise ValueError("Linha 'LPA' não encontrada no dataset")

    lpa_series = df.loc["LPA"]
    lpa_atual = lpa_series.dropna().iloc[0]
    lpa_base = lpa_atual * (1 + cagr(lpa_series)) if not np.isnan(cagr(lpa_series)) else lpa_atual

    # ---------- ROE ----------
    if "ROE" not in df.index:
        raise ValueError("Linha 'ROE' não encontrada no dataset")

    roe_series = df.loc["ROE"] / 100
    roe_atual = roe_series.dropna().iloc[0]
    roe_base = roe_atual * (1 + cagr(roe_series)) if not np.isnan(cagr(roe_series)) else roe_atual
    roe_base = min(roe_base, MAX_ROE)

    # ---------- DY / PAYOUT ----------
    payout = 0.0
    dy_base = 0.0
    
    if "D.Y" in df.index:
        dy_series = df.loc["D.Y"] / 100
        dy_atual = df.iloc[0] if not df.empty else 0.0
        dy_base = dy_atual * (1 + cagr(dy_series)) if not np.isnan(cagr(dy_series)) else dy_atual
        
        dy_clean = dy_series.dropna()

    if dy_clean.empty:
        dy_base = 0.0
    else:
        dy_base = float(dy_clean.iloc[0])
        
    if dy_base > 0:
        payout = min(dy_base, MAX_PAYOUT)    
    else:
        payout = 0.0      

    retencao = 1 - payout

    # ---------- CRESCIMENTO ----------
    g = min(roe_base * retencao, MAX_GROWTH)

    # ---------- PROJEÇÃO ----------
    lucros = [
        lpa_base * (1 + g) ** t
        for t in range(1, anos_crescimento + 1)
    ]

    vp_lucros = [
        lucro / (1 + ke) ** t
        for t, lucro in enumerate(lucros, start=1)
    ]

    # ---------- VALOR TERMINAL ----------
    lucro_terminal = lucros[-1] * (1 + g_perpetuidade)
    valor_terminal = lucro_terminal / (ke - g_perpetuidade)
    vp_terminal = valor_terminal / (1 + ke) ** anos_crescimento

    return sum(vp_lucros) + vp_terminal


# =========================
# MARKET DATA
# =========================
def get_price(
    ticker: str,
    ano: int,
    mode: str = "start"
) -> float:
    """
    Obtém a primeira ou última cotação válida de um ano.

    mode:
        - "start" → primeira cotação do ano
        - "end"   → última cotação do ano
    """
    
    if FOLDER == "IBOV" or FOLDER == "IDIV":
        ticker_obj = yf.Ticker(f"{ticker}.SA")
    else:
        ticker_obj = yf.Ticker(ticker)

    start_date = f"{ano}-01-01"
    end_date = f"{ano}-12-31"

    data = ticker_obj.history(
        start=start_date,
        end=end_date,
        interval="1d"
    )

    if data.empty:
        raise ValueError(f"Sem dados de cotação para {ticker} em {ano}")

    if mode == "start":
        price = data["Close"].iloc[0]
    elif mode == "end":
        price = data["Close"].iloc[-1]
    else:
        raise ValueError("mode deve ser 'start' ou 'end'")

    return round(float(price), 2)


# =========================
# SERVICE / ORQUESTRAÇÃO
# =========================
def analyze_ticker(
    base_path: str,
    ticker: str,
    ano: int,
    ke: float
) -> Dict[str, float]:

    df = load_financial_dataframe(f"{base_path}{ticker}.csv", ano)
    valor_intrinseco = valuation_via_roe(
        df=df,
        ke=ke,
        g_perpetuidade=0.05,
        anos_crescimento=10
    )

    preco_inicio = get_price(ticker, ano, "start")
    preco_fim = get_price(ticker, ano, "end")
    
    return {
        "ticker": ticker.upper(),
        "valor_intrinseco": round(valor_intrinseco, 2),
        "desconto_%": (round((preco_inicio - valor_intrinseco) / valor_intrinseco * 100, 2)
                            if valor_intrinseco not in (0, None, np.nan)
                            else None
                    ),
        "preco_inicio": preco_inicio,
        "preco_fim": preco_fim,
        "variacao_%": round((preco_fim - preco_inicio) / preco_inicio * 100, 2),
    }
