import math

def getRendimientoCodigo(codigo, probs, base=2) -> float:
    """
    Recibe un código junto a las probabilidades de la fuente que codifica y devuelve el valor del rendimiento del código.
    Utiliza base 2 para la entropía por defecto.
    """
    entropFuente = sum(prob * math.log(1 / prob, base) for prob in probs)
    l = sum(p * len(c) for p, c in zip(probs, codigo))

    return entropFuente / l if l != 0 else 0.0

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

def getLongMediaExtN(probs, extOrdN) -> float:
    """
    Recibe las probabilidades originales de una fuente,
    junto con las palabras código de una extensión de cualquier orden N.

    Devuelve la longitud media de esta extensión de orden N.

    Esta función está plain MAL, rehacerla o corregirla
    """
    longMed = 0
    for elem in extOrdN:
        probAct = 1
        probAct *= probs.index(simb) for simb in elem
        longMed += probAct * len(elem)
    return longMed

def cumpleTeoremaShannon(probs, extOrdN, N) -> bool:
    return getEntropBaseR(probs) <= longMediaExtN / N < getEntropBaseR(probs) + 1/N