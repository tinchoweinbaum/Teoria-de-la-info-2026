import libguia6 as lib

entrada = "abcacaabbcacaabcacaaabcaca"
print("Cadena de entrada: " + entrada)
print("Probabilidades de entrada: " + str(lib.getProbsPriori(entrada)))

salida = "01010110011001000100010011"
print("Cadena de salida: " + salida)
print("")

print("Matriz del canal: ")
matCanal = lib.getMatCanal(entrada, salida)
for fila in matCanal:
    print(fila)