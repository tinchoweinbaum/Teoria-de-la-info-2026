import libguia6 as lib

probsA = [0.7, 0.3]
canalA = [[0.7, 0.3],
          [0.4, 0.6]]

entropPrioriA = lib.getEntrop(probsA)
probSalidaA = lib.getProbSalida(canalA, probsA)
entropSalidaA = lib.getEntrop(probSalidaA)
ruidoA = lib.getEntropPosterioriMediaBaseR(canalA, probsA)
perdidaA = lib.getPerdidaTotalBaseR(canalA, probsA)
infoMediaSimultA = lib.getInfoMutua_procSimultaneo(canalA,probsA, probSalidaA)
infoMediaDifA = lib.getInfoMutua_diferencia(canalA, probsA)
entropAfinA = lib.getEntropConjunta_procSimultaneo(canalA, probsA)
entropAfinDifA = lib.getEntropConjunta_diferencia(canalA, probsA, probSalidaA)

print("Entropía a priori H(A) del Canal 1: " + str(entropPrioriA))
print("Entropía de salida H(B) del Canal 1: " + str(entropSalidaA))
print("Ruido H(A/B) del Canal 1: " + str(ruidoA))
print("Pérdida H(B/A) del Canal 1: " + str(perdidaA))
print("Información media I(A,B) del Canal 1 calculada por procesos simultáneos: " + str(infoMediaSimultA))
# print("Información media I(A,B) del Canal 1 calculada por diferencia de entropía y ruido: " + str(infoMediaDifA))
print("Entropía conjunta H(A,B) del Canal 1 calculada por la matriz de procesos simultáneos: " + str(entropAfinA))
# print("Entropía conjunta H(A,B) del Canal 1 calculada por diferencia de entropías e información mutua: " + str(entropAfinDifA))
