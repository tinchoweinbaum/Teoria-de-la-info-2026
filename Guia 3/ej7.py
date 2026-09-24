import libguia3 as lib

codigos = []

codA = ["011", "000", "010", "101", "001", "100"]
codigos.append(codA)

codB = ["110", "100", "101", "001", "110", "010"]
codigos.append(codB)

codC = ["10", "1100", "0101", "1011", "0","110"]
codigos.append(codC)

codD = ["1101", "10", "1111", "1100", "1110", "0"]
codigos.append(codD)

codE = ["011", "0111", "01", "0", "011111", "01111"]
codigos.append(codE)

codF = ["1110", "0", "110", "1101", "1011", "10"]
codigos.append(codF)

for codigo in codigos:
    print("Código: " + str(codigo))

    noSingular, instantaneo, univoco = lib.clasificarCodigo(codigo)

    if instantaneo:
        print("Código instantáneo.")
    elif univoco:
        print("Código unívoco.")
    elif noSingular:
        print("Código no singular.")
    else:
        print("Código bloque.")
    print("")