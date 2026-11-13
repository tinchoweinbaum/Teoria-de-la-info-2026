import libguia4 as lib

codA = ["0100100", "0101000", "0010010", "0100000"]
codB = ["0100100", "0010010", "0101000", "0100001"]
codC = ["0110000", "0000011", "0101101", "0100110"]

codigos = [codA, codB, codC]

for codigo in codigos:
    print(codigo)
    hamming, detectables, corregibles = lib.getHammingErrores(codigo)
    print("La distancia de hamming mínima de este codigo es " + str(hamming) + ", se pueden detectar " + str(detectables) + " errores y corregir " + str(corregibles) + ".")
    print("")