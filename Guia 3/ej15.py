import libguia3 as lib3


codigos = []

codigoA = ["==", "<", "<=", ">", ">=", "<>"]
codigos.append(codigoA)

codigoB = [")", "[]", "]]", "([", " [()]", "([)]"]
codigos.append(codigoB)

codigoC = ["/", "*", "-", "*", "++", "+-"]
codigos.append(codigoC)

codigoD = [".,", ";", ",,", ":", "...", ",:;"]
codigos.append(codigoD)

probs = [0.1, 0.5, 0.1, 0.2, 0.05, 0.05]
print("Probabilidades para todos los códigos: " + str(probs))
print("")

for codigo in codigos:
    print("Código : " + str(codigo))
    longMedia = lib3.getLongMedia(codigo, probs)
    r = len(lib3.getAlfabetoCodigo(codigo))
    entropR = lib3.getEntropBaseR(probs, r)


    noSingular, instantaneo, univoco = lib3.clasificarCodigo(codigo)

    if instantaneo:
        print("Código instantáneo.")
    elif univoco:
        print("Código unívoco.")
    elif noSingular:
        print("Código no singular.")
    else:
        print("Código bloque.")

    print("Su entropía en base " + str(r) + " es " + str(entropR))
    print("Su longitud media es " + str(longMedia))
    print("El código es compacto" if lib3.esCodigoCompacto(codigo, probs) else "El código no es compacto")
    print("")

print("")
print("")
print("")