import libguia3

codigoA = ["010", "101", "000", "111"]
codigoB = ["110", "001", "11", "00"]

print("Código 1: " + str(codigoA))
print("El código es instantáneo" if libguia3.esCodigoInstantaneo(codigoA) else "El código no es instantáneo")
print("El código es unívocamente decodificable" if libguia3.esCodigoUnivoco(codigoA) else "El código no es unívocamente decodificable")

print("")

print("Código 1: " + str(codigoB))
print("El código es instantáneo" if libguia3.esCodigoInstantaneo(codigoB) else "El código no es instantáneo")
print("El código es unívocamente decodificable" if libguia3.esCodigoUnivoco(codigoB) else "El código no es unívocamente decodificable")