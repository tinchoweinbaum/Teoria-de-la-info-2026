import math

# ---- Funciones utilizadas ----

def _getAlfabeto_mensaje(mensaje, ordenable = True):
    """
    Recibe un mensaje emitido por una fuente cualquiera y devuelve el alfabeto
    utilizado en el mensaje.
    Si ordenable es True llama a .sort antes de devolver el alfabeto

    Función "privada"
    """
    alfabeto = []
    for simb in mensaje:
        if simb not in alfabeto:
            alfabeto.append(simb)

    if ordenable: alfabeto.sort()
    
    return alfabeto

def getAlfabeto_MatTrans(mensaje: list):
    """
    Recibe un mensaje emitido por una fuente y devuelve su alfabeto y su matriz de transición
    """
    alfabeto = _getAlfabeto_mensaje(mensaje)
    cantSimbolos = [0] * len(alfabeto) # Cantidad de veces que aparece cada símbolo para calcular sus frecuencias
    matTrans = [[0] * len(alfabeto) for _ in range(len(alfabeto))]

    for elem in mensaje[:-1]:
        cantSimbolos[alfabeto.index(elem)] += 1

    for indice in range(len(mensaje) - 1):
        matTrans[alfabeto.index(mensaje[indice + 1])][alfabeto.index(mensaje[indice])] += 1/cantSimbolos[alfabeto.index(mensaje[indice])]
    return alfabeto, matTrans 

def esFuenteMemoria(matTrans, tolerancia = 0.03):
    """
    Recibe la matriz de transición de una fuente y según las probabilidades y la tolerancia ingresada, devuelve True si la fuente es de memoria.

    La diferencia entre el mayor y el menor de cada fila tiene que ser menor a la tolerancia para todas las filas
    """
    for fila in matTrans:
        if (max(fila) - min(fila)) > tolerancia:
            return True
    return False

def getVectorMarkov_analitico(matrizProbs, tolerancia=1e-6):
    """
    Recibe la matriz de transición de una fuente de Markov de orden 1 (donde las COLUMNAS suman 1)
    y devuelve su vector estacionario hallado con el método de las potencias.
    """
    n = len(matrizProbs)
    
    # Vector de probabilidad inicial con distribución uniforme
    pi = [1.0 / n] * n
    
    while True:
        pi_nuevo = [0.0] * n
        
        # Multiplicación Matriz x Vector Columna: pi_nuevo[i] = suma_j(P[i][j] * pi[j])
        for i in range(n):
            for j in range(n):
                pi_nuevo[i] += matrizProbs[i][j] * pi[j]
        
        # Cálculo del error (norma L1 de la diferencia)
        error = sum(abs(pi_nuevo[k] - pi[k]) for k in range(n))

        if error <= tolerancia:
            return pi_nuevo
            
        pi = pi_nuevo

def _getExtensionOrdN(alfabeto, n):
    """
    Recibe el alfabeto de la fuente a extender junto con el orden al que se desea extender la fuente.
    Devuelve el alfabeto de la nueva fuente, conformado por las combinaciones de los elementos del alfabeto original tomados de a n.
    Devuelve una lista de strings independientemente del tipo de dato que haya en el alfabeto.

    Función "privada"
    """
    extension = [""]

    for _ in range(n):
        nueva_extension = []
        for comb in extension:
            for elem in alfabeto:
                nueva_extension.append(comb + str(elem))
        extension = nueva_extension

    return extension

def getExtensionProbsOrdN(alfabeto, probs, n):
    """
    Recibe un alfabeto con sus probabilidades y un número entero N.
    Devuelve dos listas: La extensión de orden n junto con una lista de sus probabilidades.

    Se rompe si la fuente original tenía símbolos de más de 1 caracter, ej: "AB" como un único símbolo.
    """
    extOrdN = _getExtensionOrdN(alfabeto, n)
    probExtOrdN = [1]*len(extOrdN)

    for elem in extOrdN:
        for simb in elem:
            probExtOrdN[extOrdN.index(elem)] *= probs[alfabeto.index(simb)]

    return extOrdN, probExtOrdN

def getEntropiaMarkov(matrizProbs, vectorMarkov, base=2) -> float:
    """
    Recibe la matriz de transición y el vector estacionario de una fuente de markov junto con una base r para la entropía.
    Devuelve la entropía de la fuente markoviana en base r, por defecto r=2.
    """
    entrop = 0

    for i in range(len(vectorMarkov)):
        for j in range(len(matrizProbs[i])):
            if matrizProbs[j][i] != 0:
                entrop += vectorMarkov[i] * matrizProbs[j][i]*math.log(1/matrizProbs[j][i],base)

    return entrop

def getInfo_prob(prob):
    """
    Recibe la probabilidad de un suceso y devuelve la cantidad de información que se
    obtendría si este suceso ocurriese.
    """
    if prob != 0:
        return math.log2(1/prob)
    print("Probabilidad = 0 :/")
    return 0

def getInfo_listaProbs(listaProbs):
    """
    Recibe una lista de probabilidades de una fuente de memoria nula y devuelve
    una lista con la cantidad de información de cada suceso según su probabilidad
    """
    listaInfo = []
    for elem in listaProbs:
        listaInfo.append(getInfo_prob(elem))
    return listaInfo

def _getEntropia_listaProbs(listaProbs):
    """
    Recibe una lista de probabilidades de una fuente de memoria nula y devuelve
    una lista con la entropía de cada suceso según su probabilidad

    Función "privada"
    """
    listaInfo = getInfo_listaProbs(listaProbs)
    listaEntrop = []
    for i in range(len(listaProbs)):
        listaEntrop.append(listaInfo[i] * listaProbs[i])
    return listaEntrop

def getEntropiaFuente_listaProbs(listaProbs):
    """
    Recibe una lista de probabilidades de una fuente de memoria nula y devuelve
    el valor de la entropía de la fuente.
    """
    listaEntropia = _getEntropia_listaProbs(listaProbs)
    return sum(listaEntropia)


# ---- Invocaciones y resultados ----

mensaje = "CCAABBCCAABBCCAABBCCAABBCCAABB"

alf, matTrans = getAlfabeto_MatTrans(mensaje)

print("Mensaje: " + mensaje)
print("")

print("Alfabeto: " + str(alf))

print("Matriz de transición: ")
for fila in matTrans:
    print(fila)
print("")

tol = 1e-10
print("Con una tolerancia de " + str(tol) + ", la fuente es una")
print("fuente con memoria" if esFuenteMemoria(matTrans, tolerancia = tol) else "Fuente de memoria nula")
print("")

vecMarkov = getVectorMarkov_analitico(matTrans)
print("Vector estacionario: " + str(vecMarkov))
print("")

extOrden2, probsExt = getExtensionProbsOrdN(alf,vecMarkov, 2)
print("Extensión de orden 2 utilizando su vector estacionario: " + str(extOrden2))
print("")
print("Probabilidades de la extensión de orden 2: " + str(probsExt))
print("")

pAC = probsExt[extOrden2.index("AC")]
print("P(AC) = " + str(pAC))

pBB = probsExt[extOrden2.index("BB")]
print("P(BB) = " + str(pBB))

pCB = probsExt[extOrden2.index("CB")]
print("P(CB) = " + str(pCB))

print("")

entropMarkovBase2 = getEntropiaMarkov(matTrans,vecMarkov)
print("Entropía en base 2 de la fuente: "  + str(entropMarkovBase2))
print("")

entropExt = getEntropiaFuente_listaProbs(probsExt)
print("Entropía de la extensión de orden 2 de la fuente: "  + str(entropExt))

"""
En primer lugar para obtener la matriz de transición de la fuente de información se contabiliza la cantidad de veces que todos los símbolos se suceden entre sí, es decir que se obtiene P(Si/Sj) para todo i,j perteneciente a S. Se puede ver a simple viste que nunca se emite una A después de una B, o una B luego de una C.

Observando esta matriz, y utilizando una tolerancia de 1e-10, podemos llegar a la conclusión de la que fuente es de memoria, es decir que el símbolo emitir es estadísticamente dependiente del anteriormente emitido, con una tolerancia tan pequeña esto se puede afirmar con mucha seguridad.

Conociendo que se trata de una fuente de memoria, se puede calcular su vector estacionario, es decir, la probabilidad que se observará para cada símbolo de la fuente en un mensaje emitido en un tiempo lo suficientemente largo, esto se hizo por el método de las potencias, se iteró un vector pi inicial a través de la matriz de transición hasta que el cambio en este vector sea menor a una tolerancia de 1e-6, este vector es completamente independiente del estado inicial de la fuente.

En base a este vector se busca averiguar la extensión de orden 2 de la fuente (utilizando su vector estacionario como su propia fuente de memoria nula), tomando todos los simbolos de la fuente de a pares y obteniendo la probabilidad resultante por medio de multiplicar los siímbolos que componen a cada elemento de la extensión.

Al tratarse de una fuente de memoria, a la hora de obtener la entropía asociada a la fuente se calcula teniendo en cuenta tanto su vector estacionario como su matriz de transición. El valor de la entropía se puede interpretar de varias maneras, como por ejemplo la cantidad de información media de cada símbolo de la fuente, ponderada por las probabilidades.
Al ser un valor relativamente bajo podemos asumir que un observador estudiando los símbolos emitidos por esta fuente tendra una incertidumbre baja.

Por otro lado al calcular la entropía de la extensión de orden 2 de la fuente, se obtiene un valor independiente de su matriz de transición, y es por esto que se obtiene un valor distinto del doble de la entropía de la fuente original, recordemos que: 

H₂(S) = 2*H₂(S²)

Sin embargo esto solo se sostiene cuando se trabaja con fuentes de memoria nula, si calculásemos la entropía de la fuente original utilizando su vector estacionario como una distribución de probabilidades de una fuente sin memoria obtenemos: H₂(S) = 1.5826, lo cuál es coherente con la propiedad matemática que relaciona las entropías de una fuente de memoria nula y de sus extensiones de orden n.
"""