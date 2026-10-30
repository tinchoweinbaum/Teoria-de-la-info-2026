import libguia6 as lib

probPrioriA = [2/5, 3/5]
matCanalA = [[3/5, 2/5],
             [1/3, 2/3]]

entropPrioriA = lib.getEntrop(probPrioriA)
print("Entropía a priori de C1: " + str(entropPrioriA))
entropPostA = lib.getEntropPosterioriMediaBaseR(matCanalA, probPrioriA)
print("Ruido del Canal A: " + str(entropPostA))
listaEntrops = lib.getListaEntropsPosterioriBaseR(matCanalA, probPrioriA)
print("Entropías de cada símbolo de salida del Canal A: " + str(listaEntrops))