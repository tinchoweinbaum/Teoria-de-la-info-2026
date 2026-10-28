def _getAlfabeto(mensaje: str, ordenable = True) -> list[str]:
    """
    Recibe una cadena y devuelve el alfabeto utilizado en ella. Por defecto ordena el alfabeto obtenido.

    Función "privada".
    """
    listaRet = []
    for car in mensaje:
        if car not in listaRet:
            listaRet.append(car)
    return sorted(listaRet) if ordenable else listaRet

def getProbsPriori(mensaje: str) -> list[float]:
    """
    Recibe un mensaje de entrada y devuelve las probabilidades del mismo.
    """
    alfabeto = _getAlfabeto(mensaje)
    probs = [0] * len(alfabeto)

    lenMensaje = len(mensaje)
    for elem in mensaje:
        probs[alfabeto.index(elem)] += 1 / lenMensaje
        
    return probs

def getMatCanal(entrada: str, salida: str) -> list[list[float]]:
    """
    Recibe la entrada que pasó por un canal junto con su salida generada, devuelve la matriz calculada del canal.
    """
    alfabetoEntrada = _getAlfabeto(entrada)
    alfabetoSalida = _getAlfabeto(salida)
    filas = len(alfabetoEntrada) # Cantidad de filas y columnas (entradas y salidas)
    columnas = len(alfabetoSalida)

    cantApariciones = [0] * filas # Vector que contiene cuantas veces aparece cada símbolo de la entrada.
    for elem in entrada:
        cantApariciones[alfabetoEntrada.index(elem)] += 1

    matRet = [[0 for _ in range(columnas)] for _ in range(filas)] # Inicializa en 0 la matriz de retorno.
    for i in range(len(entrada)):
        matRet[alfabetoEntrada.index(entrada[i])][alfabetoSalida.index(salida[i])] += 1/cantApariciones[alfabetoEntrada.index(entrada[i])]
    return matRet