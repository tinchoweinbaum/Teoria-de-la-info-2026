import math

# --- Funciones utilizadas ---
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

def getCodigoHuffman_dict(probs: list[float], alfabeto: list[str]) -> dict[str, str]:
    """
    Recibe las probabilidades y los símbolos de la fuente.
    Devuelve un diccionario {simbolo: palabra_codigo} generado mediante el algoritmo de Huffman.
    """
    if len(probs) != len(alfabeto):
        return None
        
    codigos = {simbolo: "" for simbolo in alfabeto}
    
    nodos = [[p, [s]] for p, s in zip(probs, alfabeto)]
    
    while len(nodos) > 1:
        nodos.sort(key=lambda x: x[0])
    
        izq = nodos.pop(0)
        der = nodos.pop(0)
        
        # 0 p los simb de la izquierda
        for simbolo in izq[1]:
            codigos[simbolo] = "0" + codigos[simbolo]
            
        # 1 a los simb de la derecha
        for simbolo in der[1]:
            codigos[simbolo] = "1" + codigos[simbolo]
            
        # agrupa las probabilidades y concatena las listas de símbolos
        nuevo_nodo = [izq[0] + der[0], izq[1] + der[1]]
        nodos.append(nuevo_nodo)
        
    return codigos

def getCodigoHuffman(alfabeto: list[str],probs: list[float]) -> list[str]:
    """
    Recibe una lista con las probabilidades de una fuente y su alfabeto.
    Devuelve una lista con las palabras código binarias obtenidas por el algoritmo de Huffman
    """
    dictHuffman = getCodigoHuffman_dict(probs, alfabeto)
    return [dictHuffman[simbolo] for simbolo in alfabeto]

def getLongMedia(probs: list, codigo: list) -> float:
    """
    Recibe un código y su lista de probabilidades y devuelve su longitud media.
    """
    l = 0
    for i in range(len(codigo)):
        l += probs[i] * len(codigo[i])
    return l


def getRendimientoCodigo(codigo, probs, base=2) -> float:
    """
    Recibe un código junto a las probabilidades de la fuente que codifica y devuelve el valor del rendimiento del código.
    Utiliza base 2 para la entropía por defecto.
    """
    entropFuente = getEntropBaseR(probs)
    l = getLongMedia(probs, codigo)

    return entropFuente / l if l != 0 else 0.0

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


# --- Resolución del ejercicio ---

mensaje = "100110000001000000001000100000"

alf, probs = getAlfabetoProbabilidades_mensaje(mensaje)
entrop = getEntropBaseR(probs)
codigo = ["0","1"]
longMed = getLongMedia(probs, codigo)
rend = getRendimientoCodigo(codigo, probs)

ext2, probsExt2 = getExtensionProbsOrdN(alf, probs,2)
codExt2 = getCodigoHuffman(ext2, probsExt2)
longMediaExt2 = getLongMedia(probsExt2, codExt2)
rendExt2 = getRendimientoCodigo(codExt2, probsExt2)

ext3, probsExt3 = getExtensionProbsOrdN(alf, probs, 3)
codExt3 = getCodigoHuffman(ext3, probsExt3)
longMediaExt3 = getLongMedia(probsExt3, codExt3)
rendExt3 = getRendimientoCodigo(codExt3, probsExt3)

print("Las probabilidades de la fuente son: " + str(probs))
print("Entropía de la fuente: " + str(entrop))
print("La longitud media del código trivial para la fuente binaria es: " + str(longMed))
print("El rendimiento del código es: " + str(rend))
print("")

print("El código de huffman para la extensión de orden 2 es: " + str(codExt2))
print("Su longitud media es de: " + str(longMediaExt2))
print("Su rendimiento es de:" + str(rendExt2)) 
print("")

print("El código de huffman para la extensión de orden 3 es: " + str(codExt3))
print("Su longitud media es de: " + str(longMediaExt3))
print("Se rendimiento es de: " + str(rendExt3))

La entropía de la fuente original se calculó con las probabilidades observadas en el mensaje, esta entropía calculada actuará como el límite teórico de la longitud media de los códigos unívocamente decodificables que se puedan crear para esta fuente.
Al tratarse de una fuente binaria, el código óptimo se puede obtener trivialmente: [0,1], podemos ver que este código tendrá una longitud media de 1, mientras que la entropía es de 0.7219, es decir que el código obtenido, por más de ser el óptimo para esta fuente no tiene un rendimiento muy alto, esto se debe a que el número de bits en las palabras código debe ser potencia entera de las probabildades de la fuente, cosa que no ocurre en este caso.

Al extender la fuente con n = 2, y codificarla con el algoritmo de Huffman que siempre genera códigos óptimos es el siguiente: ['1', '011', '00', '010'], observamos un aumento sustancial del rendimiento, porque se acerca mucho más la entropía de la fuente extendida al código óptimo que se halló para esa. Recordemos que al extender con un orden n, la entropía de la extensión será n*H(S), mientras que este NO es el caso con la longitud media del código óptimo, por lo que al extender es posible obtener un código con mayor rendimiento.

Si se extiende una vez más la fuente con n = 3, el rendimiento mejora aún más, observamos que L es aproximadamente igual a H(S) (rendimiento de 99%), este código resulta entonces excelente para codificar mensajes de la fuente binaria. El código obtenido por Huffman es  ['1', '001', '010', '00001', '011', '00010', '00011', '00000']

Si bien es verdad que gracias al primer teorema de Shannon podemos extender la fuente todo lo que querramos para aproximar la longitud media del código a la entropía, con el fin de lograr un código con un rendimiento elevado, el costo a pagar computacionalmente es muy alto, por que con cada extensión de la fuente deberemos manejar exponencialmente más símbolos, en la extensión de orden 2 deberemos manejar 4 símbolos, en la de orden 3 serán 9 símbolos, etc.