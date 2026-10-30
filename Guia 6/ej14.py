import libguia6 as lib

probsA = [0.7, 0.3]
canalA = [[0.7, 0.3],
          [0.4, 0.6]]

entropPrioriA = lib.getEntrop(probsA)
probSalidaA = lib.getProbSalida(canalA, probsA)
entropSalidaA = lib.getEntrop(probSalidaA)
ruidoA = lib.getEntropPosterioriMediaBaseR(canalA, probsA)

print("Entropía a priori H(A) del Canal 1: " + str(entropPrioriA))
print("Entropía de salida H(B) del Canal 1: " + str(entropSalidaA))
print("Ruido H(A/B) del Canal 1: " + str(ruidoA))
