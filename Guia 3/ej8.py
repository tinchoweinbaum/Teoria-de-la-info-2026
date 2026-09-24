import libguia3 as lib

codigos = []

codigoA = ["==", "<", "<=", ">", ">=", "<>"]
codigos.append(codigoA)

codigoB = [")", "[]", "]]", "([", " [()]", "([)]"]
codigos.append(codigoB)

codigoC = ["/", "*", "-", "*", "++", "+-"]
codigos.append(codigoC)

codigoD = [".,", ";", ",,", ":", "...", ",:;"]
codigos.append(codigoD)

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