import libguia6 as lib

entradaA = "1101011001101010010101010100011111"
salidaA = "1001111111100011101101010111110110"
print("Entrada del primer canal: " + entradaA)
print("Probabilidades a priori: " + str(lib.getProbsPriori(entradaA)))
print("")

print("Salida del primer canal: " + salidaA)
print("")

print("Matriz del canal: ")
matCanalA = lib.getMatCanal(entradaA, salidaA)
for fila in matCanalA:
    print(fila)

print("")

entradaA = "110101100110101100110101100111110011"
salidaA = "110021102110022010220121122100112011"
print("Entrada del segundo canal: " + entradaA)
print("Probabilidades a priori: " + str(lib.getProbsPriori(entradaA)))
print("")

print("Salida del segundo canal: " + salidaA)
print("")

print("Matriz del canal: ")
matCanalA = lib.getMatCanal(entradaA, salidaA)
for fila in matCanalA:
    print(fila)
