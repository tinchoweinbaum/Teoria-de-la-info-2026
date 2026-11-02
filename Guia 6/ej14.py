import libguia6 as lib

probsA = [0.7, 0.3]
canalA = [[0.7, 0.3],
          [0.4, 0.6]]

print("--- CANAL 1 ---")
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

probsB = [0.5, 0.5]
canalB = [[0.3, 0.3, 0.4],
          [0.3, 0.3, 0.4]]
print("--- CANAL 2 ---")
entropPrioriB = lib.getEntrop(probsB)
probSalidaB = lib.getProbSalida(canalB, probsB)
entropSalidaB = lib.getEntrop(probSalidaB)
ruidoB = lib.getEntropPosterioriMediaBaseR(canalB, probsB)
perdidaB = lib.getPerdidaTotalBaseR(canalB, probsB)
infoMutuaB = lib.getInfoMutua_procSimultaneo(canalB, probsB, probSalidaB)
entropAfinB = lib.getEntropConjunta_procSimultaneo(canalB, probsB)

print("Entropía a priori H(A) del Canal 2: " + str(entropPrioriB))
print("Entropía de salida H(B) del Canal 2: " + str(entropSalidaB))
print("Ruido H(A/B) del Canal 2: " + str(ruidoB))
print("Pérdida H(B/A) del Canal 2: " + str(perdidaB))
print("Información mutua I(A,B) del Canal 2: " + str(infoMutuaB)) # No entiendo porque da 0, lo debería haber visto venir????
print("Entropía conjunta H(A,B) del Canal 2: " + str(entropAfinB))