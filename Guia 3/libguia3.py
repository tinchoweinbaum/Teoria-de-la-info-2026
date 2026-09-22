"""
Librería con las funciones para resolver los problemas de la guía 3.
"""

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

def esCodigoUnivoco(codigo):
    """
    Recibe un código y devuelve True si el código es instantáneo, False si no.
    """
    if (not esCodigoNoSingular(codigo)) or (not esCodigoInstantaneo(codigo)):
        return False

    # Sardinas patterson?   