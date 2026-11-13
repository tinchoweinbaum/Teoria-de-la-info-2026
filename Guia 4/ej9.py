import libguia4 as lib

codA = ["00", "01", "10", "11"]
codB = ["000", "100", "101", "111"]
codC = ["0000", "0011", "1010", "0101"]

codigos = [codA, codB, codC]

for codigo in codigos:
    print(codigo)
    detectables, corregibles = lib.getCantErroresDetectablesCorregibles(codigo)
    print("Para este código se pueden detectar " + str(detectables) + " errores y corregir " + str(corregibles))
    print("")