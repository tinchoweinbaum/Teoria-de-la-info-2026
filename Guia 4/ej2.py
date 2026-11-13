import libguia4 as lib

probs = [0.3, 0.1, 0.4, 0.2]
codigo = ["BA", "CAB", "A", "CBA"]

extOrd2, probsExt2 = lib.getExtensionProbsOrdN(codigo, probs, 2)

print("El código cumple el teorema de Shannon" if lib.cumpleShannon_extOrdN(probs, extOrd2, 2) else "El código no cumple el teorema de Shannon")