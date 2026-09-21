import libguia2

probs = [0.2, 0.1, 0.5, 0.2]
print("Probabilidades de la fuente: ")
print(probs)

print("")
print("Cantidad de información de cada símbolo según su probabilidad: ")
print(libguia2.getInfo_listaProbs(probs))

print("")
print("Entropía de los símbolos de la fuente según su probabilidad:")
print(libguia2.getEntropia_listaProbs(probs))
