import libguia6 as lib

canalA = [[0.7, 0, 0.3, 0],
          [0.2, 0.6, 0, 0.2]]
probsA = [0.5, 0.5]

canalB = [[0.9, 0, 0.1],
          [0, 1, 0],
          [0.1, 0.1, 0.8],
          [0, 0.5, 0.5]]
probsB = lib.getProbSalida(canalA, probsA)

print("Canal A: ")
for fila in canalA: print(fila)
print("Ruido o equivocación del Canal A: " + str(lib.getEntropPosterioriMediaBaseR(canalA, probsA)))
print("Información mutua del Canal A: " + str(lib.getInfoMutua_procSimultaneo(canalA, probsA, probsB)))
print("")

print("Canal B: ")
for fila in canalB: print(fila)
print("Ruido o equivocación del Canal B: " + str(lib.getEntropPosterioriMediaBaseR(canalB, probsB)))
print("Información mutua del Canal B: " + str(lib.getInfoMutua_procSimultaneo(canalB, probsB, lib.getProbSalida(canalB, probsB))))
print("")

print("Canal compuesto AB: ")
canalComp = lib.getCanalCompuesto(canalA, canalB)
for fila in canalComp: print(fila)
print("Ruido o equivocación del Canal AB: " + str(lib.getEntropPosterioriMediaBaseR(canalComp, probsA)))
print("Información mutua del Canal AB: " + str(lib.getInfoMutua_procSimultaneo(canalComp, probsA, lib.getProbSalida(canalComp, probsA))))