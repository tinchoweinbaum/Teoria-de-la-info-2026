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
    print("Código: " + str(codigo))

    noSingular, instantaneo, univoco = lib3.clasificarCodigo(codigo)

    if instantaneo:
        print("Código instantáneo.")
    elif univoco:
        print("Código unívoco.")
    elif noSingular:
        print("Código no singular.")
    else:
        print("Código bloque.")

    r = len(lib3.getAlfabetoCodigo(codigo))
    print("La entropía de la fuente en base " + str(r) + " es " + str(lib3.getEntropBaseR(probs,r)))
    print("Su longitud media es " + str(lib3.getLongMedia(codigo, probs)))
    print("")

    # Repasar la relación entre la clasificación del código, el valor de la entropía en base r y el valor de la longitud media y la inec. de kraft.