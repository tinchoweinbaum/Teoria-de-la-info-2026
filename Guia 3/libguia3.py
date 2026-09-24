"""
Librería con las funciones para resolver los problemas de la guía 3.
"""

import math

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
    """
    if not esCodigoNoSingular(codigo):
        return (False, False, False)

    if esCodigoInstantaneo(codigo):
        return (True, True, True)

    if esCodigoUnivoco(codigo):
        return (True, False, True)

    return (True, False, False) # No singular pero no instantáneo ni unívoco.

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

def _getLongPalabrasCodigo(codigo):
    """
    Recibe un código y devuelve una lista con la lóngitud de las palabras código.
    """
    listaLen = []
    for palabra in codigo:
        listaLen.append(len(palabra))
    return listaLen

def calculaInecKraft(codigo: list[str]) -> float:
    """
    Recibe un código y devuelve el valor de su inecuación de Kraft.
    """
    lenPalabras = _getLongPalabrasCodigo(codigo)
    r = len(getAlfabetoCodigo(codigo))
    kraft = 0.0

    for l in lenPalabras:
        kraft += r ** (-l)

    return kraft

def cumpleKraft(codigo: list[str]) -> bool:
    """
    Recibe un código y devuelve True si cumple la inecuación de Kraft, False si no.
    """
    return calculaInecKraft(codigo) <= 1.0

def getLongMedia(codigo: list, probs: list) -> float:
    """
    Recibe un código y su lista de probabilidades y devuelve su longitud media.
    """
    l = 0
    for i in range(len(codigo)):
        l += probs[i] * len(codigo[i])
    return l

def getEntropBaseR(probs: list[float], r: int) -> float:
    """
    Recibe una lista de probabilidades y devuelve el valor de la entropía de la fuente en base r.
    """
    entrop = 0
    for prob in probs:
        if prob > 0:
            entrop += prob * math.log(1/prob, r)
    return entrop
codigos = []