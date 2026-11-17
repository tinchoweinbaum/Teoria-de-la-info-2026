import libguia6 as lib

matCanal = [[0.6, 0.4],
            [0.2, 0.8]]
probs = [0.5, 0.5]

print("Matriz del Canal: ")
for fila in matCanal: print(fila)

print("Su probabilidad de error es: " + str(lib.getProbErrorCanal_maxProbCondicional(matCanal, probs)))