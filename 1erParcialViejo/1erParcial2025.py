import math, random

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

def imprimir_matriz(matriz, precision=4):
    """
    Imprime una matriz 2D alineando perfectamente sus columnas.
    Si hay números flotantes, los formatea con la precisión dada.
    """
    # Formatear cada elemento a string
    matriz_str = []
    for fila in matriz:
        fila_str = []
        for x in fila:
            if isinstance(x, float):
                fila_str.append(f"{x:.{precision}f}")
            else:
                fila_str.append(str(x))
        matriz_str.append(fila_str)

    # Ancho máximo de cada columna
    num_cols = len(matriz_str[0])
    anchos = [max(len(fila[c]) for fila in matriz_str) for c in range(num_cols)]

    # Imprimir alineado por columna
    for fila in matriz_str:
        print("  ".join(f"{val:>{anchos[i]}}" for i, val in enumerate(fila)))

def getVectorMarkov_analitico(matrizProbs, tolerancia=1e-7):
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

        print(pi_nuevo)

        if error <= tolerancia:
            return pi_nuevo
            
        pi = pi_nuevo

def getEntropiaMarkov(matrizProbs, vectorMarkov, base=2) -> float:
    """
    Recibe la matriz de transición y el vector estacionario de una fuente de markov junto con una base r para la entropía.
    Devuelve la entropía de la fuente markoviana en base r.
    """
    entrop = 0

    for i in range(len(vectorMarkov)):
        for j in range(len(matrizProbs[i])):
            if matrizProbs[j][i] != 0:
                entrop += vectorMarkov[i] * matrizProbs[j][i]*math.log(1/matrizProbs[j][i],base)

    return entrop

def esCodigoNoSingular(codigo):
    """
    Recibe un código y devuelve True si es NO SINGULAR.
    """
    return len(set(codigo)) == len(codigo)

def esCodigoInstantaneo(codigo):
    """
    Recibe un código y devuelve True si el código es instantáneo
    """
    for i in range(len(codigo)):
        for j in range(len(codigo)):
            if j!=i:
                if codigo[j].startswith(codigo[i]):
                    return False
    return True

def esCodigoUnivoco(codigo: list):
    """
    Recibe un código y devuelve True si el código es instantáneo, False si no.
    Ejecuta el algoritmo de Sardinas-Patterson sobre el código para verificar si es unívoco.
    Sardinas-Patterson es útil para determinar si un código no instantáneo es UD.
    """
    if esCodigoInstantaneo(codigo):
        return True

    if not esCodigoNoSingular(codigo):
        return False

    c = codigo.copy()
    sufijos = []

    for i in range(len(c)):
        for j in range(len(c)):
            if i != j:
                if c[j].startswith(c[i]):
                    sufijo = c[j].removeprefix(c[i])
                    if sufijo in c:
                        return False
                    if sufijo not in sufijos:
                        sufijos.append(sufijo) # 1er recorrido para buscar sufijos en el codigo original

    # 2do recorrido con los sufijos originales ya creados
    for sufijo in sufijos:
        for palabra in c:
            nuevo_sufijo = None

            # si la palabra del código empieza con el sufijo
            if palabra.startswith(sufijo) and palabra != sufijo:
                nuevo_sufijo = palabra.removeprefix(sufijo)

            # siel sufijo empieza con una palabra del código
            elif sufijo.startswith(palabra) and sufijo != palabra:
                nuevo_sufijo = sufijo.removeprefix(palabra)

            # si se generó un sobrante válido
            if nuevo_sufijo:
                if nuevo_sufijo in c:
                    return False

                if nuevo_sufijo not in sufijos:
                    sufijos.append(nuevo_sufijo)
    return True

def clasificarCodigo(codigo: list[str]) -> tuple:
    """
    Recibe un código y devuelve una 3-upla con la siguiente información:
    
    1er valor: True si el código es No Singular.
    2do valor: True si el código es Instantáneo.
    3er valor: True si el código es Unívoco.

    Uso: 
    noSingular, instantaneo, univoco = lib.clasificarCodigo(codigo)

    if instantaneo:
        print("Código instantáneo.")
    elif univoco:
        print("Código unívoco.")
    elif noSingular:
        print("Código no singular.")
    else:
        print("Código bloque.")
    print("")
    """
    if not esCodigoNoSingular(codigo):
        return (False, False, False)

    if esCodigoInstantaneo(codigo):
        return (True, True, True)

    if esCodigoUnivoco(codigo):
        return (True, False, True)

    return (True, False, False) # No singular pero no instantáneo ni unívoco.


def getLongMedia(codigo: list, probs: list) -> float:
    """
    Recibe un código y su lista de probabilidades y devuelve su longitud media.
    """
    l = 0
    for i in range(len(codigo)):
        l += probs[i] * len(codigo[i])
    return l

def _cantInfoBaseR(prob, r):
    """
    Recibe el valor de una única probabilidad y la base r y devuelve la cantidad de información en base r.

    Función "privada"
    """
    return math.log(1/prob, r) if prob != 0 else 0

def getAlfabetoCodigo(codigo: list[str], stringRet = False):
    """
    Recibe un código y devuelve el alfabeto código utilizado ordenado según la tabla ASCII.

    Si stringRet == True devuelve el alfabeto en un string.
    Si stringRet == False devuelve el alfabeto en una lista.
    """
    alfabeto = [] # Variable auxiliar para transformarla en string

    for palabra in codigo:
        for car in palabra:
            if car not in alfabeto:
                alfabeto.append(car)
    alfabeto.sort()

    return "".join(alfabeto) if stringRet else alfabeto

def esCodigoCompacto(codigo: list[str], probs: list[float]) -> bool:
    """
    Recibe un código y las probabilidades de la fuente que codifica.
    Devuelve True si el código es compacto, False si no.
    """
    _, esInstantaneo, _ = clasificarCodigo(codigo)

    if not esInstantaneo:
        return False

    alfabetoCodigo = getAlfabetoCodigo(codigo)
    r = len(alfabetoCodigo)
    for i in range(len(codigo)):
        print((_cantInfoBaseR(probs[i], r))) # Checkeo que todas las palaras son <= en long. que la cantidad de información del símbolo que codifican.
        if len(codigo[i]) > math.ceil(_cantInfoBaseR(probs[i], r)):
            return False

    return True

codigo = ["(]" , "]", "[)", ")", "(["]
probs = [0.15, 0.25, 0.05, 0.45, 0.1]

print("Entropía: " + str(getEntropiaFuente_listaProbs(probs)))
print("Longitud media: " + str(getLongMedia(codigo, probs)))

  
noSingular, instantaneo, univoco = clasificarCodigo(codigo)

if instantaneo:
    print("Código instantáneo.")
elif univoco:
    print("Código unívoco.")
elif noSingular:
    print("Código no singular.")
else:
    print("Código bloque.")
print("")

print("El código es compacto" if esCodigoCompacto(codigo, probs) else "El código no es compact")









