import libguia6 as lib

entrada = "abcacaabbcacaabcacaaabcaca"
salida = "01010110011001000100010011"

probsPriori = lib.getProbsPriori(entrada)
matCanal = lib.getMatCanal(entrada, salida)

probSalidaEmpirica = lib.getProbsPriori(salida) # Calcula las probabilidades de los símbolos de salida de manera empírica
probSalidaTeorica = lib.getProbSalida(matCanal, probsPriori)

print("Probabilidades de salida observadas: " + str(probSalidaEmpirica))
print("")

print("Probabilidades de salida calculadas: " + str(probSalidaTeorica))