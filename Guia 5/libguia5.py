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

def getByteArrayRLC(mensaje):
    """
    Recibe un mensaje y devuelve un bytearray que contiene el mensaje comprimido con RLC.
    Usa un byte para almacenar el ASCII del caracter y otro byte para el número de apariciones consecutivas.
    """
    pass