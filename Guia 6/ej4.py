import libguia6 as lib

print("Canal binario sin ruido equiprobable:")
matCanal = [[1,0],
            [0,1]]
for fila in matCanal:
    print(fila)
print("")

probsPriori = [0.5, 0.5]
probsSalida = lib.getProbSalida(matCanal, probsPriori)
print("Probabilidades de salida: ")
print(probsSalida)
print("")

matPosteriori = lib.getMatProbPosteriori(matCanal, probsPriori, probsSalida)
print("Probabilidades a posteriori:")
for fila in matPosteriori:
    print(fila)