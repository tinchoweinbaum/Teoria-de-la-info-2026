import libguia3 as lib

codigo = ["110", "100", "101", "001", "110", "01"]

print("Código: " + str(codigo))
lenPalabras = lib._getLongPalabrasCodigo(codigo)
print("Longitud de las palabras código: " + str(lenPalabras))
alfabeto = lib.getAlfabetoCodigo(codigo, stringRet=True)
print("Alfabeto código: " + str(alfabeto))
print("La inecuació de kraft para este código es " + str(lib.calculaInecKraft(codigo)))
print("Cumple la inecuación de Kraft" if lib.cumpleKraft(codigo) else "No cumple la inecuación de kraft")