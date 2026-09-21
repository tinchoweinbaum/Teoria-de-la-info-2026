import libguia2

mensaje = "ABDAACAABACADAABDAADABDAAABDCDCDCDC"

alf, probs = libguia2.getAlfabetoProbabilidades_mensaje(mensaje)

print("Mensaje emitido por la fuente: " + mensaje)
print("Alfabeto de la fuente: " + str(alf))
print("Distribución de probabilidades de la fuente: " + str(probs))
print("Entropía de la fuente: " + str(libguia2.getEntropiaFuente_listaProbs(probs)))