import pandas as pd
import matplotlib.pyplot as plt

def gerar_dashboard(resultados, plot):
    # =========================
    # DATAFRAME CONSOLIDADO
    # =========================
    df = pd.DataFrame([{
        "id": r.id,
        "status": r.status.value,
        "tentativas": r.tentativa,
        "duracao_seg": (r.fim - r.inicio).total_seconds(),
        "erro": r.erro
    } for r in resultados])

    # =========================
    # VISÃO EXECUTIVA (TEXTO)
    # =========================
    print("\n📊 DASHBOARD DE EXECUÇÃO")
    print(df.groupby("status")["id"].count())

    print("\n⏱️ TEMPO MÉDIO POR STATUS (s)")
    print(df.groupby("status")["duracao_seg"].mean())

    # =========================
    # GRÁFICO DE BARRAS – TEMPO POR ITEM
    # =========================
    
    if plot:
        plt.figure()
        plt.bar(df["id"], df["duracao_seg"])
        plt.xlabel("ID do Item")
        plt.ylabel("Tempo de Execução (segundos)")
        plt.title("Tempo de Execução por Item")

        # 🔒 FORÇA EIXO X COMO INTEIRO
        plt.xticks(df["id"])   

        plt.tight_layout()
        plt.show()

    return df

def salvar_relatorio(df):
    df.to_csv("reports/relatorio_execucao.csv", index=False)
