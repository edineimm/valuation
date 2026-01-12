from concurrent.futures import ThreadPoolExecutor, as_completed
from core.process import processar_item
from core.config import THREAD_WORKERS

def executar_paralelo_thread(fila, workers=THREAD_WORKERS):
    resultados = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(processar_item, item): item for item in fila}

        for future in as_completed(futures):
            resultados.append(future.result())

    return resultados
