import libguia3

codA = ['100', '10','1000','0']
codB = ['011', '0', '01', '011']

print("Codigo A: " + str(codA))
print("El código es no singular" if libguia3.esCodigoNoSingular(codA) else "El código es singular")

print("")

print("Código B: " + str(codB))
print("El código es no singular" if libguia3.esCodigoNoSingular(codB) else "El código es singular")
