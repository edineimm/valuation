import pandas as pd

def gerar_handbook(resultados):
    """
    Gera o handbook operacional do RPA com:
    - Key Item
    - Status
    - Mensagem de Exceção (se houver)
    """

    handbook = pd.DataFrame([{
        "key_item": int(item.id),
        "status": item.status.value,
        "mensagem_excecao": (
            item.erro.splitlines()[-1] if item.erro else ""
        )
    } for item in resultados])

    return handbook

def exibir_handbook(handbook):
    print("\n📘 HANDBOOK OPERACIONAL - RESULTADO DA EXECUÇÃO\n")
    print(handbook.to_string(index=False))

def salvar_handbook(handbook, nome_arquivo="reports/handbook_execucao.csv"):
    handbook.to_csv(nome_arquivo, index=False)
