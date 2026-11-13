import math

# --- Funciones de guías anteriores ---

def _getCantInfoBaseR(prob, r = 2) -> float:
    """
    Recibe una base logarítmica r y una probabilidad.
    Devuelve la cantidad de información en base r asociada a la probabilidad.
    
    Se usa r = 2 si no se especifica un valor.
    Devuelve 0 si la probabilidad es 0.
    """
    return math.log(1/prob,r) if prob > 0 else 0

def getEntropBaseR(probs, r = 2) -> float:
    """
    Recibe la lista de probabilidades de una fuente y una base logarítmica r (por defecto 2).
    Devuelve la entropía base r de la fuente.
    Se ignoran sucesos con probabilidad 0.
    """
    return sum(prob * _getCantInfoBaseR(prob, r) for prob in probs)

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
    
    # Calculamos las combinaciones de probabilidad igual que en la función de Shannon
    probExtOrdN = probs[:]
    for _ in range(n - 1):
        probExtOrdN = [p * q for p in probExtOrdN for q in probs]

    return extOrdN, probExtOrdN

def getLongMedia(probs: list, codigo: list) -> float:
    """
    Recibe un código y su lista de probabilidades y devuelve su longitud media.
    """
    l = 0
    for i in range(len(codigo)):
        l += probs[i] * len(codigo[i])
    return l

# --- Funciones de esta guía ---

def _getRendimientoCodigo(codigo, probs, base=2) -> float:
    """
    Recibe un código junto a las probabilidades de la fuente que codifica y devuelve el valor del rendimiento del código.
    Utiliza base 2 para la entropía por defecto.
    """
    entropFuente = sum(prob * math.log(1 / prob, base) for prob in probs)
    l = sum(p * len(c) for p, c in zip(probs, codigo))

    return entropFuente / l if l != 0 else 0.0

def cumpleShannon_extOrdN(probs: list[float], extOrdN: list[str], n: int) -> bool:
    """
    Recibe una lista con las probabilidades de la fuente, junto con las palabras código de la extensión de orden n y el valor de n.
    Devuelve True si el código cumple el primer teorema de Shannon, False si no.
    """
    entropExtN = getEntropBaseR(probs) * n

    probsExt = probs[:] # Calculo las probabilidades de la extensión por medio de hacer las combinaciones entre las probabilidades.
    for _ in range(n - 1):
        probsExt = [p * q for p in probsExt for q in probs]

    longMed = 0
    for i in range(len(probsExt)):
        longMed += probsExt[i] * len(extOrdN[i])

    # print("Entropía Calculada: " + str(entropExtN))
    # print("Longitud media calculada: " + str(longMed))

    return entropExtN <= longMed < entropExtN + 1

def cumpleShannon(probs, codigo):
    """
    Recibe una distribución de probabilidades junto a una lista de palabras código.
    Devuelve True si el código cumple el 1er teorema de Shannon.
    """
    entrop = getEntropBaseR(probs)
    longMed = getLongMedia(probs, codigo)

    return entrop <= longMed < entrop + 1



def getCodigoHuffman_dict(probs: list[float], alfabeto: list[str]) -> dict[str, str]:
    """
    Recibe las probabilidades y los símbolos de la fuente.
    Devuelve un diccionario {simbolo: palabra_codigo} generado mediante el algoritmo de Huffman.
    """
    if len(probs) != len(alfabeto):
        return None
        
    # Diccionario para ir armando las palabras código de atrás para adelante
    codigos = {simbolo: "" for simbolo in alfabeto}
    
    # Cada "nodo" es una lista simple: [probabilidad_acumulada, [lista_de_simbolos]]
    nodos = [[p, [s]] for p, s in zip(probs, alfabeto)]
    
    while len(nodos) > 1:
        # Ordenamos de menor a mayor probabilidad
        nodos.sort(key=lambda x: x[0])
        
        # Extraemos los dos con menor probabilidad
        izq = nodos.pop(0)
        der = nodos.pop(0)
        
        # A todos los símbolos del grupo izquierdo les anteponemos un '0'
        for simbolo in izq[1]:
            codigos[simbolo] = "0" + codigos[simbolo]
            
        # A todos los símbolos del grupo derecho les anteponemos un '1'
        for simbolo in der[1]:
            codigos[simbolo] = "1" + codigos[simbolo]
            
        # Agrupamos las probabilidades y concatenamos las listas de símbolos
        nuevo_nodo = [izq[0] + der[0], izq[1] + der[1]]
        nodos.append(nuevo_nodo)
        
    return codigos

def getCodigoHuffman(probs: list[float], alfabeto: list[str]) -> list[str]:
    """
    Recibe una lista con las probabilidades de una fuente y su alfabeto.
    Devuelve una lista con las palabras código binarias obtenidas por el algoritmo de Huffman
    """
    dictHuffman = getCodigoHuffman_dict(probs, alfabeto)
    return [dictHuffman[simbolo] for simbolo in alfabeto]

def getRedundanciaRendimiento(probs: list[float], codigo: list[str]) -> tuple[float, float]:
    """
    Recibe una distribución de probabilidades de una fuente y su código y devuelve una tupla con el rendimiento y la redundancia de código.
    """
    return _getRendimientoCodigo(codigo, probs), 1 - _getRendimientoCodigo(codigo, probs) # a mi que me importa la memoria

def getDistHamming(cadA: str, cadB: str) -> int:
    """
    Recibe dos cadenas y devuelve la distancia de hamming entre ellas.
    Si las cadenas son de distinta longitud devuelve None.
    """
    if len(cadA) != len(cadB):
        return None
    
    dist = 0
    for i in range(len(cadA)):
        if(cadA[i] != cadB[i]):
            dist += 1
    return dist

def getMinDistHammingCodigo(codigo: list[str]) -> int:
    """
    Recibe un código y devuelve cuál es la menor distancia de hamming entre cualquiera de sus palabras.
    """
    return min(getDistHamming(codigo[i], codigo[j]) for i in range(len(codigo)) for j in range(i + 1, len(codigo)))

def getCantErroresDetectablesCorregibles(codigo: list[str]) -> tuple[int, int]:
    """
    Recibe un código y devuelve una tupla que indica:
    cuantos errores se pueden DETECTAR y cuantos errores se pueden CORREGIR
    """
    minHamming = getMinDistHammingCodigo(codigo)
    return minHamming - 1, math.floor((minHamming - 1)/2)

def getHammingErrores(codigo: list[str]) -> tuple[int, int, int]:
    """
    Recibe un código y devuelve una tupla que indica:
        Mínima distancia de hamming del código.
        Cantidad de errores detectables
        Cantidad de errores corregibles.
    """
    detectables, corregibles = getCantErroresDetectablesCorregibles(codigo)
    return getMinDistHammingCodigo(codigo), detectables, corregibles
    
