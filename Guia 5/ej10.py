import libguia5 as lib

mensajeA = "XXXYZZZZ"
rlcA = lib.codificaRLC(mensajeA)
print("Mensaje original: " + mensajeA)
print("Mensaje codificado con RLC: " + rlcA)
print("")

mensajeB = "AAAABBBCCDAA"
rlcB = lib.codificaRLC(mensajeB)
print("Mensaje original: " + mensajeB)
print("Mensaje codificado con RLC: " + rlcB)
print("")

mensajeC = "UUOOOOAAAIEUUUU"
rlcC = lib.codificaRLC(mensajeC)
print("Mensaje original: " + mensajeC)
print("Mensaje codificado con RLC: " + rlcC)
print("")