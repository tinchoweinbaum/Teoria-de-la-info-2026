import libguia2

alf1 = ["x", "y", "z"]
probs1 = [0.5, 0.1, 0.4]

alf2 = ["0", "1"]
probs2 = [0.5, 0.5]

alf3 = ["A", "B", "C", "D"]
probs3 = [0.1, 0.3, 0.4, 0.2]

print("Alfabeto 1: " + str(alf1))
print("Probabilidades: " + str(probs1))
print("Entropia de la fuente 1: " + str(libguia2.getEntropiaFuente_listaProbs(probs1)))
extOrd2, probsExtOrd2 = libguia2.getExtensionProbsOrdN(alf1, probs1, 2)
print("Extension de orden 2: " + str(extOrd2))
print("Entropía de la extensión de orden 2: " + str(libguia2.getEntropiaFuente_listaProbs(probsExtOrd2)))