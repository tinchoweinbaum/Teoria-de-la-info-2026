import libguia6 as lib

probsPriori = [0.2, 0.8]
matCanal = [[1,0],
            [0,1]]

probsSalida = lib.getProbSalida(matCanal, probsPriori)
print("Probabilidades de salida: " + str(probsSalida))
print("")

probsPosteriori = lib.getMatProbPosteriori(matCanal,probsPriori,probsSalida)
print("Matriz de probabilidades a posteriori: ")
for fila in probsPosteriori:
    print(fila)
print("")

matSimultaneo = lib.getMatProcesoSimultaneo_priori(matCanal, probsPriori) # También funciona calculándolo usando las probs. de salida :D
print("Matriz de procesos simultáneos: ")
for fila in matSimultaneo:
    print(fila)