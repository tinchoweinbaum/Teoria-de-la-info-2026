import libguia6 as lib

matCanal = [[0.6, 0.3, 0.1],
            [0.1, 0.8, 0.1],
            [0.3, 0.3, 0.4]]
probsA = [1/3, 1/3, 1/3]
probsB = [1/8, 3/8, 4/8]
probsC = [4/15, 3/15, 8/15]
probs = [probsA, probsB, probsC]

print("Matriz del Canal: ")
for fila in matCanal: print(fila)

for prob in probs:
    print("Distribución de probabilidades de entrada: " + str(prob))
    print("Con esta distribución de probabilidades de entrada, la probabilidad de error del canal es " + str(lib.getProbErrorCanal(matCanal, prob)))
    print("")