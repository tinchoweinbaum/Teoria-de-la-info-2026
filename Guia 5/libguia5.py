import math

# --- Funciones de guías anteriores necesarias ---
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

def getCodigoHuffman_dict(probs: list[float], alfabeto: list[str]) -> dict[str, str]:
    """
    Recibe las probabilidades y los símbolos de la fuente.
    Devuelve un diccionario {simbolo: palabra_codigo} generado mediante el algoritmo de Huffman.
    """        
    codigos = {simbolo: "" for simbolo in alfabeto}
    
    nodos = [[p, [s]] for p, s in zip(probs, alfabeto)]
    
    while len(nodos) > 1:
        nodos.sort(key=lambda x: x[0])
   
        izq = nodos.pop(0)
        der = nodos.pop(0)
        
        for simbolo in izq[1]:
            codigos[simbolo] = "0" + codigos[simbolo]
            
        for simbolo in der[1]:
            codigos[simbolo] = "1" + codigos[simbolo]

        nuevo_nodo = [izq[0] + der[0], izq[1] + der[1]]
        nodos.append(nuevo_nodo)
        
    return codigos

def getCodigoHuffman(probs: list[float]) -> list[str]:
    """
    Recibe una lista con las probabilidades de una fuente y su alfabeto.
    Devuelve una lista con las palabras código binarias obtenidas por el algoritmo de Huffman
    """
    alfabeto = [str(i) for i in range(len(probs))]
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

# --- Funciones de esta guía ---
def getCodigoShannonFano(probs: list[float]) -> list[str]:
    """
    Recibe las probabilidades y los símbolos de la fuente.
    Devuelve un código obtenido por el algoritmo de Shannon-Fano.

    Los códigos generados por Shannon-Fano son subóptimos y tienen la cota superior
    L <= H(S) + 2
    """
    alfabeto = [str(i) for i in range(len(probs))]
    # ordena decreciente
    pares = sorted(zip(probs, alfabeto), key=lambda x: x[0], reverse=True)
    codigos = {simbolo: "" for simbolo in alfabeto}

    # cola con los bloques que faltan dividir
    pendientes = [pares]

    while pendientes:
        bloque = pendientes.pop(0)

        if len(bloque) <= 1:
            continue

        # punto de corte x diferencia
        mejor_k = 1
        menor_dif = float("inf")

        for k in range(1, len(bloque)):
            suma_sup = sum(p for p, _ in bloque[:k])
            suma_inf = sum(p for p, _ in bloque[k:])
            dif = round(abs(suma_sup - suma_inf), 10)

            if dif < menor_dif:
                menor_dif = dif
                mejor_k = k

        superior = bloque[:mejor_k]
        inferior = bloque[mejor_k:]

        # 1 a la parte superior, 0 a la parte inferior
        for _, simbolo in superior:
            codigos[simbolo] += "1"
        for _, simbolo in inferior:
            codigos[simbolo] += "0"

        pendientes.append(superior)
        pendientes.append(inferior)

    return [codigos[simbolo] for simbolo in alfabeto]

def getHuffmanShannonFano(probs: list[float]) -> tuple[list[str], list[str]]: # NO USAR ESTA FUNCIÓN.
    """
    Recibe una lista con las probabilidades de una fuente y devuelve una tupla con el código de Huffman y el de Shannon-Fano.
    """
    alfabeto_aux = [str(i) for i in range(len(probs))]
    return getCodigoHuffman(alfabeto_aux, probs), getCodigoShannonFano(probs, alfabeto_aux)

def codificaRLC(mensaje: str) -> str:
    """
    Recibe una cadena y la comprime utilizando el algoritmo Run Length Encoding.

    Checkear con algún clanker.
    """
    if mensaje == "":
        return mensaje
    
    cadenaRet = ""
    charAct = mensaje[0]
    nroCharAct = 0

    for char in mensaje:
        if charAct == char:
            nroCharAct += 1
        else:
            cadenaRet += (charAct + str(nroCharAct))
            charAct = char
            nroCharAct = 1
    cadenaRet += (charAct + str(nroCharAct)) # Agrega el último caracter.

    return cadenaRet

def codificaMensaje(alfabeto: list[str], codigo: list[str], mensaje: str) -> str:
    """
    Recibe un alfabeto fuente junto a un código y un mensaje escrito en el alfabeto fuente indicado.
    Devuelve el mensaje codificado utilizando las palabras código en una cadena de caracteres.
    """
    simbArmado = ""
    mensajeCodificado = ""
    for elem in mensaje:            
        simbArmado += elem
        if simbArmado in alfabeto:
            mensajeCodificado += codigo[alfabeto.index(simbArmado)]
            simbArmado = ""

    return mensajeCodificado

def codificaMensajeCodigoBinario_bytearray(alfabeto: list[str], codigo: list[str], mensajeOriginal: str) -> bytearray:
    """
    Recibe un alfabeto fuente junto a un código binario y un mensaje escrito en el alfabeto fuente indicado.
    Devuelve el mensaje codificado utilizando las palabras código en un bytearray.
    """
    datos = bytearray()
    if mensajeOriginal == "":
        return datos

    simbArmado = ""
    mensajeCodificado = ""
    for elem in mensajeOriginal:            
        simbArmado += elem
        if simbArmado in alfabeto:
            mensajeCodificado += codigo[alfabeto.index(simbArmado)]
            simbArmado = ""

    relleno = (8 - len(mensajeCodificado) % 8) % 8
    mensajeCodificado += "0" * relleno
    datos.append(relleno)

    # 3. Corto de a 8 caracteres, casteo de binario a int y guardo el byte
    for i in range(0, len(mensajeCodificado), 8):
        bloque = mensajeCodificado[i:i+8]
        datos.append(int(bloque, 2))

    return datos

def decodificaMensajeCodigoBinario_bytearray(alfabeto: str, codigo: list[str], mensajeCodificado: bytearray) -> str:
    """
    Recibe un alfabeto fuente, su lista de palabras código binarias y un bytearray codificado.
    Devuelve el mensaje original decodificado.
    """
    if len(mensajeCodificado) == 0:
        return ""

    # 1. Leo el primer byte para saber cuántos ceros de relleno hay al final
    relleno = mensajeCodificado[0]

    # 2. Reconstruyo la tira de '0' y '1' casteando cada byte a binario de 8 bits
    cadena_bits = ""
    for byte in mensajeCodificado[1:]:
        cadena_bits += bin(byte)[2:].zfill(8)

    # 3. Vuelo los ceros de relleno del final
    if relleno > 0:
        cadena_bits = cadena_bits[:-relleno]

    # 4. Traduzco bit a bit hasta completar una palabra código
    palabraArmada = ""
    mensajeDecodificado = ""
    for bit in cadena_bits:
        palabraArmada += bit
        if palabraArmada in codigo:
            mensajeDecodificado += alfabeto[codigo.index(palabraArmada)]
            palabraArmada = ""

    return mensajeDecodificado

def getTasaCompresion(mensaje: str, datos: bytearray) -> float:
    """
    Recibe el mensaje original y el bytearray codificado.
    Devuelve la tasa de compresión (tamaño original / tamaño comprimido).
    """
    if len(datos) == 0:
        return 0.0

    return len(mensaje) / len(datos)