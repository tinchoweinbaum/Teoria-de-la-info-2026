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
            matPosteriori[i][j] = (matCanal[i][j] * probsPriori[i]) / probsSalida[j] if probsSalida[j] != 0 else 0
            
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
        entrop += prob * math.log(1 / prob, r) if prob != 0 else 0
    return entrop

# --- Funciones de Entropia a posteriori H(A/B)(ruido o equivocación) ---

def getEntropPosterioriBaseR_simbolo(matPosteriori, alfabetoSalida, b, r=2):
    """
    No voy a usar jamás esta función en mi vida.
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

# --- Funciones de pérdida H(B/A) ---

def _getPerdidaBaseR_index(matCanal, fila, r=2) -> float:
    """
    Recibe la matriz del canal, la fila del simbolo a calcular la péridad y una base logarítmica para la entropía, por defecto 2.

    Devuelve la pérdida asociada a este símbolo de entrada. H(B/ai)

    La pérdida es la incertidumbre sobre que símbolo va a aparecer en la salida conociendo la entrada (preguntar esta definición)
    """
    perdida = 0
    for prob in matCanal[fila]:
        perdida += prob * math.log(1/prob,r) if prob != 0 else 0
    return perdida

def getListaPerdidaBaseR(matCanal, r=2) -> list[float]:
    """
    Recibe la matriz del canal junto a una base logarítmica r para la entropía, por defecto 2.
    Devuelve una lista con la pérdida asociada a cada uno de los símbolos de entrada del canal H(B/ai)
    La pérdida es la incertidumbre sobre que símbolo va a aparecer en la salida conociendo la entrada (preguntar esta definición)
    """
    cantEntradas = len(matCanal)
    listaPerdida = [0] * cantEntradas
    for i in range(cantEntradas):
        listaPerdida[i] = _getPerdidaBaseR_index(matCanal, i, r)
    return listaPerdida

def getPerdidaTotalBaseR(matCanal, probsPriori, r=2) -> float:
    perdidaTotal = 0
    for i in range(len(probsPriori)):
        perdidaTotal += probsPriori[i] * _getPerdidaBaseR_index(matCanal, i, r)
    return perdidaTotal

# --- Funciones de Información mutua I(A,B) ---

def getInfoMutua_procSimultaneo(matCanal, probsPriori, probSalida, r=2) -> float:
    """
    Recibe la matriz de procesos simultáneos, las probabilidades de entrada y de salida del canal, y una base logarítmica, por defecto 2.
    Devuelve la información mutua del canal calculándola usando la matriz de procesos simultáneos: I(A,B)

    La información mutua del canal representa la cantidad de información sobre la entrada A que sobrevive al paso por el canal.
    """
    infoMedia = 0
    matSimultaneo = getMatProcesoSimultaneo_priori(matCanal, probsPriori)
    entradas = len(matSimultaneo)
    salidas = len(matSimultaneo[0])

    for i in range(entradas):
        for j in range(salidas):
            infoMedia += matSimultaneo[i][j] * math.log(matSimultaneo[i][j]/(probsPriori[i] * probSalida[j]), r) if matSimultaneo[i][j] != 0 else 0 # la simultanea depende de las de entrada y salida, no hace falta checkearlas, si es distinta de 0 las otras 2 tambien
    return infoMedia

def getInfoMutua_diferencia(matCanal, probsPriori) -> float:
    """
    Recibe la matriz de procesos simultáneos, las probabilidades de entrada y de salida del canal, y una base logarítmica, por defecto 2.
    Devuelve la información mutua del canal calculando la diferencia entre la entropía a priori y el ruido del canal: I(A,B)

    La información mutua del canal representa la cantidad de información sobre la entrada A que sobrevive al paso por el canal.
    """
    entropPriori = getEntrop(probsPriori)
    ruido = getEntropPosterioriMediaBaseR(matCanal, probsPriori)
    return entropPriori - ruido

# --- Funciones de entropía conjunta o afín H(A,B) ---

def getEntropConjunta_procSimultaneo(matCanal, probsPriori, r=2) -> float:
    """
    Recibe la matriz del canal y las probabilidads a priori junto a una base logarítmica, por defecto 2.
    Devuelve la entropía conjunta, también llamada entropía afín H(A,B), calculada por medio de la suma de las entropías
    de todos las combinaciones de entrada/salida posibles.

    La entropía conjunta H(A,B) representa la incertidumbre sobre la entrada y la salida a la vez sin conocer ninguna de las 2.
    """
    matSimultaneo = getMatProcesoSimultaneo_priori(matCanal, probsPriori)
    entropAfin = 0
    filas = len(matSimultaneo)
    columnas = len(matSimultaneo[0])

    for i in range(filas):
        for j in range(columnas):
            entropAfin += matSimultaneo[i][j] * math.log(1/matSimultaneo[i][j], r) if matSimultaneo[i][j] != 0 else 0
    return entropAfin

def getEntropConjunta_diferencia(matCanal, probsPriori, probSalida) -> float:
    """
    Recibe la matriz del canal junto con las probabilidades a priori y de salida del canal.
    Devuelve la entropía afín o conjunta H(A,B) del canal calculándola con la diferencia de entropías y de información mutua.

    La entropía conjunta H(A,B) representa la incertidumbre sobre la entrada y la salida a la vez sin conocer ninguna de las 2.
    """
    infoMutua = getInfoMutua_procSimultaneo(matCanal, probsPriori, probSalida)
    return getEntrop(probSalida) + getEntrop(probsPriori) - infoMutua
 # ----

def esCanalSinRuido(matCanal) -> bool:
    """
    Recibe la matriz de un canal y devuelve True si el canal es sin ruido.
    Un canal es sin ruido si en todas las columnas existe un único elemento != 0.

    En un canal sin ruido, H(A/B) = 0 y la información mutua es igual a la entropía de entrada.
    H(A) = I(A,B)
    """
    filas = len(matCanal)
    columnas = len(matCanal[0])

    for j in range(columnas):
        encontrado = False
        for i in range(filas):
            if matCanal[i][j] != 0 and not encontrado:
                encontrado = True
            elif matCanal[i][j] != 0:
                return False
        if not encontrado:
            return False
    return True

def esCanalDeterminante(matCanal) -> bool:
    """
    Recibe la matriz de un canal y devuelve True si este es determinante.
    Un canal es determinante si en todas sus filas existe un único elemento != 0

    En un canal determinante, la pérdida H(B/A) es 0, y se conoce con certeza la salida si se conoce previamente la entrada
    H(B) = I(A,B)
    """
    return all(any(elem == 1 for elem in fila) for fila in matCanal)

def getCanalCompuesto(canalA, canalB) -> list[list[float]]:
    """
    Recibe dos matrices que representan cada una a un canal y devuelve el canal compuesto por medio de multiplicar las matrices

    Si las matrices no son multiplicables devuelve None
    """
    if len(canalA[0]) != len(canalB):
        return None

    filas = len(canalA)
    columnas = len(canalB[0])

    canalComp = [[0.0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            for k in range(len(canalA[i])):
                canalComp[i][j] += canalA[i][k] * canalB[k][j]
    
    return canalComp

def _checkColumnasReducibles(matCanal, columnaA, columnaB) -> tuple[bool, float]:
    """
    Recibe un canal junto a dos indices de columnas dentro de la matriz.
    Devuelve True y el valor del coeficiente lineal si las dos columnas indicadas son linealmente dependientes (reducibles entre sí).
    """
    refA = 0
    refB = 0

    for fila in matCanal:
        if fila[columnaA] != 0 or fila[columnaB] != 0:
            refA = fila[columnaA]
            refB = fila[columnaB]
            break
            
    if refA == 0 and refB == 0:
        return True, 0
    
    for fila in matCanal:
        if fila[columnaA] * refB != fila[columnaB] * refA:
            return False, 0
            
    coef = refA / refB if refB != 0 else 0 
    return True, coef

def _getCanalDeterminanteCombinacion(matCanal, columnaA, columnaB):
    """
    Recibe un canal junto a dos índices de columnas dentro de la matriz.

    Si las columnas no son LD devuelve None.
    Si se pueden reducir devuelve el canal determinante necesario para poner en serie con el canal original para lograr la reducción.
    """
    reducibles, coef = _checkColumnasReducibles(matCanal, columnaA, columnaB)
    
    if not reducibles:
        return None

    columnas = len(matCanal[0])
    col_mantener = min(columnaA, columnaB)
    col_eliminar = max(columnaA, columnaB)

    # Inicializamos la matriz llena de ceros
    matDeterminista = [[0.0] * (columnas - 1) for _ in range(columnas)]

    for i in range(columnas):
        if i == col_eliminar:
            destino = col_mantener
        else:
            # Si ya pasamos la columna eliminada, los índices se desfasan en 1
            destino = i if i < col_eliminar else i - 1
            
        matDeterminista[i][destino] = 1.0

    return matDeterminista

def reduceCanal(matCanal) -> list[list[float]]:
    """
    Recibe la matriz de un canal y la reduce a su mínima expresión componiéndola
    con canales determinantes iterativamente hasta que no queden columnas linealmente dependientes.

    Preguntar como puede ser que reducir un canal reduzca el ruido y/o la equivocación del canal?? no es el mismo canal???
    """
    # shallow copy porque las listas son inmutables :p
    canalReducido = [fila[:] for fila in matCanal]
    
    hubo_reduccion = True
    
    while hubo_reduccion:
        hubo_reduccion = False
        columnas = len(canalReducido[0])
        
        # busca parejas de columnas reducibles
        for i in range(columnas):
            for j in range(i + 1, columnas):
                reducibles, coef = _checkColumnasReducibles(canalReducido, i, j)
                
                if reducibles:
                    matDeterminante = _getCanalDeterminanteCombinacion(canalReducido, i, j)
                    canalReducido = getCanalCompuesto(canalReducido, matDeterminante) # Obtiene el canal reducido por composición con un canal determinante
                    
                    # rompe el forloop
                    hubo_reduccion = True
                    break
            
            if hubo_reduccion:
                break # rompe el for exterior también
                
    return canalReducido

def esCanalBSC(matCanal: list[list[float]]) -> bool:
    """
    Recibe la matriz de un canal y devuelve True si corresponde a la de un canal BSC (Binary symmetric chanel)
    """
    if len(matCanal) != 2 or any(len(fila) != 2 for fila in matCanal):
        return False

    return (
        math.isclose(matCanal[0][0], matCanal[1][1], abs_tol=1e-9)
        and math.isclose(matCanal[0][1], matCanal[1][0], abs_tol=1e-9)
    )


def getCapacidadCanal(matCanal: list[list[float]]) -> float | None:
    """
    Calcula la capacidad del canal si es Determinante, Sin Ruido o Binario Simétrico (BSC).
    Si no cumple ninguno, lo reduce hasta llegar a un caso base o devuelve None en caso de que no sea ninguna de esas 3 cosas.
    """
    matActual = matCanal

    while True:
        if esCanalDeterminante(matActual):
            return math.log2(len(matActual[0]))

        if esCanalSinRuido(matActual):
            return math.log2(len(matActual))

        if esCanalBSC(matActual):
            p = matActual[0][1]
            if math.isclose(p, 0.0, abs_tol=1e-9) or math.isclose(p, 1.0, abs_tol=1e-9):
                return 1.0
            h_p = -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)
            return 1.0 - h_p

        matReducida = reduceCanal(matActual)

        if matReducida is None or len(matReducida[0]) == len(matActual[0]):
            return None

        matActual = matReducida

def getCapacidadEstimada(matCanal: list[list[float]], paso: float) -> tuple[float, list[float]]:
    """
    Recibe la matriz de un canal BINARIO junto a un valor de paso que se utiliza en cada iteración para probar la distribución óptima.
    Devuelve la mayor capacidad encontrada usando un valor de paso de manera estimativa junto con la distribución de probabilidades que maximiza la capacidad.
    """
    maxInfoMutua = -1
    probsOptimas = []

    for i in range(round(1 / paso) + 1):
        p = min(1.0, i * paso)
        probsAct = [p, 1.0 - p]
        infoMutuaAct = getInfoMutua_procSimultaneo(matCanal, probsAct, getProbSalida(matCanal, probsAct))
        if infoMutuaAct > maxInfoMutua:
            maxInfoMutua = infoMutuaAct
            probsOptimas = probsAct

    return maxInfoMutua, probsOptimas

def _getProbErrorSimbolo(matCanal: list[list[float]], probsPriori: list[float], indexSimbolo: int) -> float:
    """
    Recibe la matriz del canal, las probabilidades de entrada de la fuente y el index del símbolo a calcularle la probabilidad de error.
    Devuelve la probabilidad de error usando la regla de decisión de máxima posibilidad condicional.

    Función "privada"
    """
    probSalida = getProbSalida(matCanal, probsPriori)
    matPosteriori = getMatProbPosteriori(matCanal, probsPriori, probSalida)

    # regla de decisión que minimice probabilidad de error:
    salidas = [fila[indexSimbolo] for fila in matPosteriori]
    return 1 - max(salidas)

def getProbErrorCanal(matCanal: list[list[float]], probsPriori: list[float]) -> float:
    """
    Recibe la matriz del canal junto a las probabilidades de entrada de la fuente.
    Devuelve la probabilidad de error total del canal
    """
    probError = 0
    probSalida = getProbSalida(matCanal, probsPriori)
    for i in range(len(matCanal[0])):
        probError += _getProbErrorSimbolo(matCanal, probsPriori, i) * probSalida[i] # que me importa a mi la memoria calculo 1000 veces la matriz a posteriori y las probs de salida
    return probError