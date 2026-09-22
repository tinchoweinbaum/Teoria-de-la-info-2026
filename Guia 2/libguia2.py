"""
Vale la pena modelar los elementos de la materia con Clases? Crear la clase Fuente y darle métodos tipo getEntropia
"""

import math
import random

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

def getAlfabetoProbabilidades_mensaje(mensaje):
    """
    Recibe un mensaje emitido por una fuente de memoria nula y devuelve su alfabeto y
    las probabilidades de cada símbolo.
    """
    alfabeto = _getAlfabeto_mensaje(mensaje)
    probs = [0] * len(alfabeto)

    for simb in mensaje:
        probs[alfabeto.index(simb)] += 1/len(mensaje)

    return alfabeto, probs

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
    """
    extOrdN = _getExtensionOrdN(alfabeto, n)
    probExtOrdN = [1]*len(extOrdN)

    for elem in extOrdN:
        for simb in elem:
            probExtOrdN[extOrdN.index(elem)] *= probs[alfabeto.index(simb)]

    return extOrdN, probExtOrdN

def getVectorMarkov_simulacion(matrizProbs, iteraciones = 100000):
    """
    Recibe la matriz de transición de una fuente de Markov de orden 1 y devuelve su vector
    de transición hallado de manera empírica.

    Preguntar si este método tiene alguna ventaja o es mejor hacerlo analíticamente el 100% de las veces

    Preguntar si la matriz se suma 1 en las filas o en las columnas, y si se puede devolver la traspuesta
    """
    vecMarkov = [0] * len(matrizProbs)

    estados = list(range(len(matrizProbs)))
    estadoAct = random.choice(estados)

    for _ in range(iteraciones):
        estadoNew = random.choices(estados, weights = matrizProbs[estadoAct], k=1)[0]
        vecMarkov[estadoNew] += 1/iteraciones
        estadoAct = estadoNew

    return vecMarkov

def getVectorMarkov_analitico(matrizProbs, tolerancia = 1e-6):
    """
    Recibe la matriz de transición de una fuente de Markov de orden 1 y devuelve su vector
    de transición hallado de manera analítica con el método de las potencias.

    Es más eficiente que la versión empírica.

    PREGUNTAR EL ORDEN DE LA MATRIZ!!!!! LAS FILAS O LAS COLUMNAS SUMAN 1??????????????

    PREGUNTAR COMO HACER PARA SABER SI UNA FUENTE ES DE MEMORIA O NO!!!!!!!!!
    """
    n = len(matrizProbs)
    
    # Vector de probabilidad inicial con distribución uniforme
    pi = [1.0 / n] * n
    
    while True:
        pi_nuevo = [0.0] * n
        
        for i in range(n): # Itera vectores pi hasta que la tolerancia sea menor al cambio.
            for j in range(n):
                pi_nuevo[j] += pi[i] * matrizProbs[i][j]
        
        # Cálculo del error (norma L1 de la diferencia)
        error = sum(abs(pi_nuevo[k] - pi[k]) for k in range(n))
        
        # Condición de corte
        if error <= tolerancia:
            return pi_nuevo
            
        pi = pi_nuevo

def getEntropiaMarkov(matrizProbs, vectorMarkov):
    entrop = 0

    for i in range(len(vectorMarkov)):
        for j in range(len(matrizProbs[i])):
            if matrizProbs[i][j] != 0:
                entrop += vectorMarkov[i] * matrizProbs[i][j]*math.log2(1/matrizProbs[i][j])

    return entrop

def getAlfabeto_MatTrans(mensaje: list):
    """
    Recibe un mensaje emitido por una fuente y devuelve su alfabeto y su matriz de transición (asumiendo que es una fuente de Markov de orden 1)
    """
    alfabeto = _getAlfabeto_mensaje(mensaje)
    cantSimbolos = [0] * len(alfabeto) # Cantidad de veces que aparece cada símbolo para calcular sus frecuencias
    matTrans = [[0] * len(alfabeto) for _ in range(len(alfabeto))]

    for elem in mensaje[:-1]:
        cantSimbolos[alfabeto.index(elem)] += 1

    for indice in range(len(mensaje) - 1):
        matTrans[alfabeto.index(mensaje[indice])][alfabeto.index(mensaje[indice + 1])] += 1/cantSimbolos[alfabeto.index(mensaje[indice])]
    return alfabeto, matTrans 

def simularMensaje(longMensaje, alfabeto, matTrans):
    """
    Recibe un número entero, el alfabeto de una fuente y su matriz de transición.
    Devuelve un string simulado de la fuente.
    """

    simbActual = random.choice(alfabeto) # Elijo un símbolo inicial al azar
    mensaje = ""

    for i in range(longMensaje):
        mensaje += simbActual # Funciona bien con mensajes cortos pero los strings son inmutables, crea un objeto String nuevo en cada vuelta 
        simbActual = random.choices(alfabeto, weights = matTrans[alfabeto.index(simbActual)],k = 1)[0]
    return mensaje