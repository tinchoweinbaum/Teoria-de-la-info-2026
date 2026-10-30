import libguia6 as lib

entrada = "abcacaabbcacaabcacaaabcaca"
salida = "01010110011001000100010011"

probsPriori = lib.getProbsPriori(entrada)
matCanal = lib.getMatCanal(entrada, salida)

probSalida = lib.getProbSalida(matCanal, probsPriori)
matPosteriori = lib.getMatProbPosteriori(matCanal, probsPriori, probSalida)

print("Matriz de probabilidades a posteriori: ")
for fila in matPosteriori: print(fila)
print("")

matSimultaneos = lib.getMatProcesoSimultaneo_priori(matCanal, probsPriori)
for fila in matSimultaneos: print(fila)