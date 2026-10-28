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

def getProbSalida(matCanal, probsPriori) -> list[float]:
    """
    Recibe la matriz de un canal junto con las probabilidades a priori de la fuente y devuelve una lista con las probabilidades de salida de cada símbolo de salida.

    La probabilidad de salida representa la probabilidad "absoluta" de recibir un símbolo b del alfabeto de salida del canal: P(bᵢ)

    (preguntar si esta interpretación está bien)
    """
    cantSalidas = len(matCanal[0]) # Cantidad de simbolos de salida del canal.
    cantEntradas = len(matCanal) # Cantidad de símbolos de entrada del canal.
    listaProbs = [0] * cantSalidas

    for i in range(cantSalidas):
        for j in range(cantEntradas):
            listaProbs[i] += matCanal[j][i] * probsPriori[j]
    return listaProbs

def getMatProbPosteriori(matCanal, probsPriori, probsSalida) -> list[list[float]]:
    """
    Recibe la matriz del canal junto con las probabilidades de entrada y salida de los simbolos de entrada y salida respectivamente.

    Devuelve la matriz de probabilidades a posteriori del canal.

    La probabilidad a posteriori de un símbolo 'a' del alfabeto de entrada A del canal es la probabilidad de haber recibido 'a' conociendo la salida 'b': P(aᵢ/bⱼ)
    """
    filas = len(matCanal)
    columnas = len(matCanal[0])
    matPosteriori = [[0.0 for _ in range(columnas)] for _ in range(filas)]

    # i recorre las filas (entradas), j recorre las columnas (salidas)
    for i in range(filas):
        for j in range(columnas):
            matPosteriori[i][j] = (matCanal[i][j] * probsPriori[i]) / probsSalida[j]
            
    return matPosteriori