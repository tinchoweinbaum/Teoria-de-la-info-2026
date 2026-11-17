import math

# --- Funciones utilizadas ---

def getEntrop(probs, r=2):
    """
    Recibe las probabilidades de entrada o de salida del canal y la base logarítmica de la entropía, por defecto 2.

    Devuelve la entropía de entrada/salida, aka la entropía de toda la vida.
    """
    entrop = 0
    for prob in probs:
        entrop += prob * math.log(1 / prob, r) if prob != 0 else 0
    return entrop

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


def getInfoMutua_diferencia(matCanal, probsPriori) -> float:
    """
    Recibe la matriz de procesos simultáneos, las probabilidades de entrada y de salida del canal, y una base logarítmica, por defecto 2.
    Devuelve la información mutua del canal calculando la diferencia entre la entropía a priori y el ruido del canal: I(A,B)

    La información mutua del canal representa la cantidad de información sobre la entrada A que sobrevive al paso por el canal.
    """
    entropPriori = getEntrop(probsPriori)
    ruido = getEntropPosterioriMediaBaseR(matCanal, probsPriori)
    return entropPriori - ruido

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
        infoMutuaAct = getInfoMutua_diferencia(matCanal, probsAct)
        if infoMutuaAct > maxInfoMutua:
            maxInfoMutua = infoMutuaAct
            probsOptimas = probsAct

    return maxInfoMutua, probsOptimas

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

def _getProbErrorSimbolo_maxProbCondicional(matCanal: list[list[float]], probsPriori: list[float], indexSimbolo: int) -> float:
    """
    Recibe la matriz del canal, las probabilidades de entrada de la fuente y el index del símbolo a calcularle la probabilidad de error.
    Devuelve la probabilidad de error usando la regla de decisión de máxima posibilidad condicional.

    Función "privada"
    """
    columna = [fila[indexSimbolo] for fila in matCanal]
    fila_ganadora = columna.index(max(columna))

    probError = 0.0
    for i in range(len(matCanal)):
        if i != fila_ganadora:
            probError += probsPriori[i] * matCanal[i][indexSimbolo]

    return probError

def getProbErrorCanal_maxProbCondicional(matCanal: list[list[float]], probsPriori: list[float]) -> float:
    """
    Recibe la matriz del canal junto a las probabilidades de entrada de la fuente.
    Devuelve la probabilidad de error total del canal calculada con el criterio de máxima probabilidad condicional

    regla de máxima posibilidad = regla de máxima probabilidad condicional (ESTA FUNCIÓN).
    """
    probError = 0.0
    for i in range(len(matCanal[0])):
        probError += _getProbErrorSimbolo_maxProbCondicional(matCanal, probsPriori, i)
    return probError

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

# --- Resolución del ejercicio ---

canalA = [[0, 0.5, 0, 0.5],
          [0.7, 0, 0.3, 0]]
reducidoA = reduceCanal(canalA) # Reduzco a canal binario para poder hallar capacidad.
cap, probsOptimas = getCapacidadEstimada(reducidoA, 0.05)
probsOptimas = [0.5, 0.5]
ruidoA = getEntropPosterioriMediaBaseR(canalA, probsOptimas)
perdidaA = getPerdidaTotalBaseR(canalA, probsOptimas)
infoMutuaA = getInfoMutua_diferencia(canalA, probsOptimas)
probErrorA = getProbErrorCanal_maxProbCondicional(canalA, probsOptimas)

canalB = [[1,0],
          [0,1],
          [1,0],
          [0,1]]
probsB = getProbSalida(canalA, probsOptimas) # La salida de A es la entrada de B
print(probsB)
ruidoB = getEntropPosterioriMediaBaseR(canalB, probsB)
perdidaB = getPerdidaTotalBaseR(canalB, probsB)
infoMutuaB = getInfoMutua_diferencia(canalB, probsB)
probErrorB = getProbErrorCanal_maxProbCondicional(canalB, probsB)

canalCompuesto = getCanalCompuesto(canalA, canalB)
ruidoC = getEntropPosterioriMediaBaseR(canalCompuesto, probsOptimas) # La misma entrada
perdidaC = getPerdidaTotalBaseR(canalCompuesto, probsOptimas)
infoMutuaC = getInfoMutua_diferencia(canalCompuesto, probsOptimas)
probErrorC = getProbErrorCanal_maxProbCondicional(canalCompuesto, probsOptimas)

print("Primer canal: ")
for fila in canalA: print(fila)
print("Las probabilidades óptimas a priori son: " + str(probsOptimas))
print("El ruido H(A/B) del canal es: " + str(ruidoA))
print("La pérdida H(B/A) del canal es: " + str(perdidaA))
print("La información mutua del canal es: " + str(infoMutuaA))
print("La probabilidad de error P(E) total del canal es: " + str(probErrorA))
print("")

print("Segundo canal: ")
for fila in canalB: print(fila)
print("El ruido H(A/B) del segundo canal es: " + str(ruidoB))
print("La pérdida H(B/A) del segundo canal es: " + str(perdidaB))
print("La información mutua I(A,B) del segundo canal es: " + str(infoMutuaB))
print("La probabilidad de error P(E) total del segundo canal es: " + str(probErrorB))
print("")

print("Canal compuesto: ")
for fila in canalCompuesto: print(fila)
print("El ruido H(A/B) del canal compuesto es: " + str(ruidoC))
print("La pérdida H(B/A) del canal compuesto es: " + str(perdidaC))
print("La información mutua I(A,B) del canal compuesto es:" + str(infoMutuaC))
print("La probabilidad de error P(E) total del canal compuesto es: " + str(probErrorC))

Primer Canal:
Al estudiar este canal vemos que se trata de un canal sin ruido, o sea que H(A/B) = 0, lo que significa que no existe ninguna incertidumbre sobre la entrada si se conoce de antemano la salida, y esto se mantiene porque existe un único elemento distinto de 0 por cada columna.
Este no es el caso con la pérdida H(B/A), que representa la incertidumbre acerca de la salida si previamente se conoce cuál fue la entrada, ya que existe más de un elemento distinto de 0 por fila, lo que no nos permite saber con certeza que símbolo fue la salida del canal.
La información mutua será igual a la entropía a priori H(A), ya que al no haber ruido en el canal, toda la información que lo atraviese sobrevivirá intacta, como se refleja en la ecuación I(A,B) = H(A) - H(A/B)
Sin embargo, se puede ver que existe una dependencia lineal entre la primera columna y la tercera, y otra entre la segunda columna y la cuarta, por lo que es posible reducir este canal de manera suficiente (sin sufrir pérdida de información mutua), al hacerlo vemos que se obtiene un canal BSC (binario simétrico), por lo que podremos estimar más facilmente la probabilidades de entrada óptimas que maximizan la capacidad C y la información mutua del canal. 
De esta manera se puede intuír que las probabilidades óptimas de entrada serán [0.5, 0.5]

Segundo Canal:
Este canal es un canal determinante, es decir, que la pérdida H(B/A) del mismo es 0, lo que quiere decir que no existe incertidumbre alguna sobre la salida conociendo la entrada, debido a que al haber un único elemento distinto de 0 en la fila se puede saber a simple vista cuál será la salida.
El ruido del canal es igual a la pérdida del canal A, ya que la salida del canal A es la entrada del canal B, al ser el ruido la incertidumbre sobre la entrada conociendo la salida y la pérdida la incertidumbre sobre la salida conociendo la entrada, sus roles se ven invertidos al salir de un canal y entrar en el otro.
Sin embargo, la probabilidad de error calculada es distinta de 0, esto es así porque al existir más de un elemento distinto de 0 por columna, si asumimos con una regla de decisión d(bj) que dada una salida bj, la entrada fue la de máxima probabilidad a*, estaremos equivocados el 40% de las veces.
Esta chance de error es dependiente de la probabilidad de los símbolos de entrada y de las probabilidades condicionales de la matriz, entonces por ejemplo: si se observa un 0 en la salida, la entrada puede haber sido tanto A como C, pero al ser A más probable que C en la entrada, asumimos por regla de decisión que la entrada fue A, y estaremos equivocados el 40% de las veces.
En el caso de observar un 1 en la salida, al ser B y D equiprobables, es indistinto cuál elijamos por regla de decisión, la probabilidad de error asociada al símbolo de salida 1 será la misma.

Canal Compuesto:
En el caso del canal compuesto se obtiene un canal con métricas perfectas, sin ruido ni pérdida, y con la misma información mutua que el primer canal. Esto se debe a que el segundo canal es en realidad el canal determinante necesario que se debe poner en serie con el primero para lograr una reducción suficiente (sin pérdida de información mutua).
La probabilidad de error, la pérdida y el ruido resultan nulos en este caso porque podemos saber con certeza cual será la salida conociendo la entrada, y viceversa, por lo que toda la información que atraviesa el canal sale intacta por la salida y no existe ningún tipo de incertidumbre en cuanto a la entrada o la salida del canal.