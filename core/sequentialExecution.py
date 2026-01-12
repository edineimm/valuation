from core.process import processar_item

def executar_sequencial(fila):
    resultados = []

    for item in fila:
        resultado = processar_item(item)
        resultados.append(resultado)

    return resultados
