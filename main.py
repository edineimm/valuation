import pandas as pd
from queueItems import carregar_fila
from core.sequentialExecution import executar_sequencial
from core.parallelExecutionThread import executar_paralelo_thread
from core.parallelExecutionWithCPU import executar_paralelo_process
from core.dashboard import gerar_dashboard, salvar_relatorio
from core.handbook import gerar_handbook, exibir_handbook, salvar_handbook
from core.process import consolidar_dataframe
from graphs import graph
from datetime import datetime

# arquivos que mudam: carregar_fila() e executar_automacao()

def main():
    inicio = datetime.now()
    
    fila = carregar_fila()

    # Escolha o modo
    # resultados = executar_sequencial(fila) # Nada muda
    resultados = executar_paralelo_process(fila) # Nada muda

    df = gerar_dashboard(resultados, plot=False) # valuation
    salvar_relatorio(df)
    df = consolidar_dataframe(resultados) # Consolida os dados dos itens em um DataFrame
    print("\n📊 DATAFRAME FINAL")
    graph(df, True)
    
    # # Handbook
    # handbook = gerar_handbook(resultados)
    # exibir_handbook(handbook)
    # salvar_handbook(handbook)
    
    fim = datetime.now()
    
    duracao = (fim - inicio).total_seconds()
    print(f"\nTempo de execução: {duracao:.2f}s")
    
if __name__ == "__main__":
    main()
