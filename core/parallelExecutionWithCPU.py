from concurrent.futures import ProcessPoolExecutor
from core.process import processar_item
from core.config import THREAD_WORKERS

def executar_paralelo_process(fila, workers=THREAD_WORKERS):
    
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(processar_item, fila))
