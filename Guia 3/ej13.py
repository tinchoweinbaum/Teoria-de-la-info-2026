import libguia3 as lib3

fuenteA = [0.5, 0.25, 0.125, 0.125]
print("Probabilidades de la fuente 1: " + str(fuenteA))
print("")

codigoBinarioA = ["1", "01", "001", "000"]
print("Código binario propuesto: " + str(codigoBinarioA))
print("El código es compacto" if lib3.esCodigoCompacto(codigoBinarioA, fuenteA) else "El código no es compacto")

print("")

codigoTernarioA = ["1", "22", "21", "23"]
print("Código ternario propuesto: " + str(codigoTernarioA))
print("El código es compacto" if lib3.esCodigoCompacto(codigoTernarioA, fuenteA) else "El código no es compacto")

print("" \
"")

fuenteB = [1/3, 1/3, 1/6, 1/6]

print("Probabilidades de la fuente 2: " + str(fuenteB))
print("")

codigoBinarioB = ["10", "11", "001", "000"]
print("Código binario propuesto: " + str(codigoBinarioB))
print("El código es compacto" if lib3.esCodigoCompacto(codigoBinarioB, fuenteB) else "El código no es compacto")

print("")

codigoTernarioB = ["1", "2", "31", "32"]
print("Código ternario propuesto: " + str(codigoTernarioB))
print("El código es compacto" if lib3.esCodigoCompacto(codigoTernarioB, fuenteB) else "El código no es compacto")

