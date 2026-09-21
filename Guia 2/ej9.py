import libguia2

probabilidades = [0.25, 0.75, 0.5, 1, 0]

print("Probabilidades de fuente binaria a evaluar: " + str(probabilidades))
print("")

for prob in probabilidades:
    print("Probabilidad de la fuente: " + str(prob))
    print("Entropía de la fuente: " + str(libguia2.getEntropFuenteBinaria(prob)))
    print("")