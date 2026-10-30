import libguia6 as lib

probsPriori = [0.3, 0.3, 0.4]
matCanal = [[0.4, 0.4, 0.2],
            [0.3, 0.2, 0.5],
            [0.3, 0.4, 0.3]]

probSalida = lib.getProbSalida(matCanal, probsPriori)
print("Probabilidades de salida: " + str(probSalida))
print("")

matProbsPosteriori = lib.getMatProbPosteriori(matCanal, probsPriori, probSalida)
print("Matriz de probabilidades a posteriori: ")
for fila in matProbsPosteriori:
    print(fila)
print("")

matProbSimultaneo = lib.getMatProcesoSimultaneo_salida(matProbsPosteriori, probSalida)
print("Matriz de procesos simultáneos: ")
for fila in matProbSimultaneo:
    print(fila)