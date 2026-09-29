import math

# ---- Funciones utilizadas ----

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

def getEntropBaseR(probs: list[float], r: int) -> float:
    """
    Recibe una lista de probabilidades y devuelve el valor de la entropía de la fuente en base r.
    """
    entrop = 0
    for prob in probs:
        if prob > 0:
            entrop += prob * math.log(1/prob, r)
    return entrop

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

def esCodigoCompacto(codigo: list[str], probs: list[float]) -> bool:
    """
    Recibe un código y las probabilidades de la fuente que codifica.
    Devuelve True si el código es compacto, False si no.
    """
    esUnivoco = esCodigoUnivoco(codigo)

    if not esUnivoco:
        return False

    alfabetoCodigo = getAlfabetoCodigo(codigo)
    r = len(alfabetoCodigo)
    for i in range(len(codigo)): # Checkeo que todas las palaras son <= en long. que la cantidad de información del símbolo que codifican.
        if len(codigo[i]) > math.ceil(_cantInfoBaseR(probs[i], r)):
            return False

# ---- Invocaciones y resultados ----

codigo = ["A", "AB", "BC", "B", "CA"]
probs = [1/3, 1/9, 1/9, 1/3, 1/9]
alf = getAlfabetoCodigo(codigo, stringRet=True)

print("Palabras código: " + str(codigo))
print("Alfabeto código: " + alf)
print("Probabilidades de la fuente: " + str(probs))
print("")

kraft = calculaInecKraft(codigo)
print("Inecuación de Kraft-McMillan: " + str(kraft))
print("")

entrop = getEntropBaseR(probs, r = len(alf))
print("Entropía de la fuente (Base 3): " + str(entrop))
print("")

longMed = getLongMedia(codigo, probs)
print("Longitud media del código: " + str(longMed))
print("")

print("El código es compacto" if esCodigoCompacto(codigo, probs) else "El código no es compacto")

"""
Para comenzar, a simple vista se puede asegurar que el código no es instantáneo ya que hay palabras código que son prefijo de otras: A es prefijo de AB y B es prefijo de BC, no podemos entonces asegurar que el código sea unívoco ni compacto por ahora.

Luego se calcula la inecuación de Kraft sobre el código dado, es importante notar que este valor depende únicamente de las longitudes de las palabras código y NO de las probabilidades de la fuente que se codifica.
Con el resultado obtenido, no podemos decir con certeza si el código es unívoco o no, porque el cumplimiento de la inecuación de Kraft es una condición necesaria pero no suficiente para clasificar un código como unívocamente decodificable, podemos asegurar en cambio que existe un código instantáneo (y por lo tanto unívocamente decodificable) con las mismas longitudes que el código estudiado.

Al tener un alfabeto de 3 símbolos, en pos de poder comparar la entropía de la fuente con su longitud media, se tomará 3 como base logarítmica.
Por otro lado, al calcular la longitud media del código, por medio de hallar el promedio de las longitudes de las palabras ponderadas por su respectiva probabilidad, llegamos a que es exactamente igual a la entropía, esto significa que en caso de ser compacto, será un código óptimo, ya que aprovecharía cada bit de información que se utiliza para representar sus mensajes al 100%
Esto es posible porque las probabilidades de la fuente son potencias enteras inversas de la longitud del alfabeto código que se usa como base logarítmica.

Sin embargo, para poder asegurar que se trata de un código compacto necesitamos saber primeramente si este es unívocamente decodificable, cosa que no podemos asegurar de antemano porque el mismo no es instantáneo, ni desmentir porque la inecuación de Kraft se cumple, entonces, una manera de demostrar esto es con el algoritmo de Sardinas-Patterson, o más facilmente con un contraejemplo de una cadena emitida por la fuente que presente ambigüedades:

Si se recibiese el mensaje ABA, no sería posible determinar si el mensaje emitido por la fuente fue S₁S₄S₁ o S₂S₁, queda demostrado entonces que este código NO es unívocamente decodificable, y por extensión NO es compacto, ya que la univocidad es un requerimiento de los códigos compactos, por más de cumplir todos los otros requerimientos.
De igual manera en el programa se ejecuta el algoritmo de Sardinas-Patterson y se puede ver que este devuelve False.

Un posible código compacto con el mismo alfabeto es entonces C = {A, CA, CB, B, CC}
Este código no contiene prefijos, lo que lo hace instantáneo y a su vez unívocamente decodificable, al tener exactamente las mismas longitudes que el código original podemos asegurar con certeza que el código es compacto.
Esto también es posible demostrarlo calculando la cantidad de información en base 3 para todos los símbolos de la fuente, y verificando que todas las palabras código propuestas coinciden con este valor en su longitud, es decir: I(Si) = li para todos los símbolos de la fuente. 


"""