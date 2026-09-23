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

            # Si se generó un sobrante válido
            if nuevo_sufijo:
                if nuevo_sufijo in c:
                    return False

                if nuevo_sufijo not in sufijos:
                    sufijos.append(nuevo_sufijo)
    return True