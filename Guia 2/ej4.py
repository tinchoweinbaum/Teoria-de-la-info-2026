import libguia2

alf1 = ["x","y","z"]
probs1 = [0.5, 0.1 ,0.4]

alf2 = [0, 1]
probs2 = [0.5, 0.5]

alf3 = ["A", "B", "C", "D"]
probs3 = [0.1, 0.3, 0.4, 0.2]

print("Alfabeto de la fuente 1: " + str(alf1))
print("Cantidad de información por símbolo: " + str(libguia2.getInfo_listaProbs(probs1)))
print("Entropía de la fuente: " + str(libguia2.getEntropiaFuente_listaProbs(probs1)))
print("")

print("Alfabeto de la fuente 1: " + str(alf2))
print("Cantidad de información por símbolo: " + str(libguia2.getInfo_listaProbs(probs2)))
print("Entropía de la fuente: " + str(libguia2.getEntropiaFuente_listaProbs(probs2)))
print("")


print("Alfabeto de la fuente 1: " + str(alf3))
print("Cantidad de información por símbolo: " + str(libguia2.getInfo_listaProbs(probs3)))
print("Entropía de la fuente: " + str(libguia2.getEntropiaFuente_listaProbs(probs3)))
print("")
