import math


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

    Para cada elemento de la matriz, P(bj/ai) es la probabilidad de observar bj en la salida sabiendo que la entrada fue ai
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

    P(bj) es la probabilidad de observar bj en la salida sin conocer el símbolo de entrada.
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

def getMatProcesoSimultaneo_priori(matCanal, probsPriori: list[float]) -> list[list[float]]:
    """
    Recibe la matriz del canal juntos con las probabilidades a PRIORI de la fuente.
    Devuelve la matriz de procesos simultáneos.

    La matriz de procesos simultáneos contiene en cada posición la probabilidad de que se den a y b simultáneamente: P(ai,bj).
    """
    filas = len(matCanal)
    columnas = len(matCanal[0])
    matSimultaneo = [[0.0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            matSimultaneo[i][j] = matCanal[i][j] * probsPriori[i]

    return matSimultaneo

def getMatProcesoSimultaneo_salida(matPosteriori, probsSalida: list[float]) -> list[list[float]]:
    """
    Recibe la matriz de probabilidades a posteriori juntos con las probabilidades de las SALIDAS P(bi) de la fuente.
    Devuelve la matriz de procesos simultáneos.

    La matriz de procesos simultáneos contiene en cada posición la probabilidad de que se den a y b simultáneamente: P(ai,bj).
    """
    filas = len(matPosteriori)
    columnas = len(matPosteriori[0])
    matSimultaneo = [[0.0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            matSimultaneo[i][j] = matPosteriori[i][j] * probsSalida[j]

    return matSimultaneo

def getEntrop(probs, r=2):
    """
    Recibe las probabilidades de entrada o de salida del canal y la base logarítmica de la entropía, por defecto 2.

    Devuelve la entropía de entrada/salida, aka la entropía de toda la vida.
    """
    entrop = 0
    for prob in probs:
        entrop += prob * math.log(1/prob,r)
    return entrop

# --- Funciones de Entropia a posteriori H(A/B)(ruido) ---

def getEntropPosterioriBaseR_simbolo(matPosteriori, alfabetoSalida, b, r=2):
    """
    Recibe la matriz de probabilidades a posteriori del canal junto a su alfabeto de salida, el símbolo b a calcular su entropía junto a la base logarítmica de la entropía, por defecto 2.

    Devuelve la entropía a posteriori asociada al símbolo de salida bj.

    H(A/bj) representa la incertidumbre del observador sobre la entrada, conociendo que la salida fue bj.
    """
    columna = alfabetoSalida.index(b)
    entropPosteriori = 0

    for fila in matPosteriori:
        entropPosteriori += fila[columna] * math.log(1/fila[columna],r) if fila[columna] != 0 else 0
    return entropPosteriori

def getListaEntropsPosterioriBaseR(matCanal, probsPriori, r=2):
    """
    Recibe la matriz del canal junto con las probabilidades a priori y la base logarítimica r para la entropía, por defecto 2.

    Devuelve una LISTA con las entropías en base r de cada uno de los símbolos de salida: H(A/bj)
    """
    probSalida = getProbSalida(matCanal, probsPriori)
    matPosteriori = getMatProbPosteriori(matCanal, probsPriori, probSalida)

    cantSalidas = len(matCanal[0])
    listaEntrops = [0] * cantSalidas
    for i in range(cantSalidas):
        listaEntrops[i] = _getEntropPosterioriBaseR_index(matPosteriori, i, r)
    return listaEntrops


def _getEntropPosterioriBaseR_index(matPosteriori, columna, r=2):
    """
    Recibe la matriz de probabilidades a posteriori del canal, junto con la columna del símbolo del que se desea averiguar la entropía y la base logarítmica para la entropía, por defecto 2.

    Devuelve la entropía a posteriori asociada al símbolo de salida en la columna indicada.

    H(A/bj) representa la incertidumbre del observador sobre la entrada, conociendo que la salida fue bj.

    Función "privada"
    """
    entropPosteriori = 0

    for fila in matPosteriori:
        entropPosteriori += fila[columna] * math.log(1/fila[columna],r) if fila[columna] != 0 else 0
    return entropPosteriori

def getEntropPosterioriMediaBaseR(matCanal, probsPriori, r=2):
    """
    Función wrapper de la que calcula la entropía para que tenga una interfaz más simple.

    Recibe la matriz del canal y las probabilidades a priori.
    Devuelve la entropía MEDIA a posteriori del canal: H(A/B)

    La entropía media a posteriori del canal se denomina "ruido" o "equivocación" y representa cuanta información se pierde por las distorsiones del canal.
    """
    probSalida = getProbSalida(matCanal, probsPriori)
    matPosteriori = getMatProbPosteriori(matCanal, probsPriori, probSalida)
    return _getEntropPosterioriMediaBaseR(matPosteriori, probSalida, r)

def _getEntropPosterioriMediaBaseR(matPosteriori, probSalida, r=2):
    """
    Recibe la matriz a posteriori del canal junto con la base logarítmica r para la entropía, por defecto 2.

    Devuelve la entropía MEDIA a posteriori del canal: H(A/B)

    La entropía media a posteriori del canal se denomina "ruido" o "equivocación" y representa cuanta información se pierde por las distorsiones del canal.

    Función "privada".
    """
    entropPosterioriMedia = 0
    for i in range(len(matPosteriori[0])): # Se puede usar cualquier fila
        entropPosterioriMedia += probSalida[i] * _getEntropPosterioriBaseR_index(matPosteriori, i, r)
    return entropPosterioriMedia # o ruido ¯\_(ツ)_/¯

# --- Funciones de Equivocación H(B/A)