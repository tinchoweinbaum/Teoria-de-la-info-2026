import libguia3 as lib3

codigoA = ["==", "<", "<=", ">", ">=", "<>"]
probs = probs = [0.1, 0.5, 0.1, 0.2, 0.05, 0.05]


print("Código: " + str(codigoA))
print("Probabilidades de la fuente: " + str(probs))
print("")

for _ in range(200):
    print(lib3.simulaMensajeCodificado(codigoA, probs, 6))
    print("")