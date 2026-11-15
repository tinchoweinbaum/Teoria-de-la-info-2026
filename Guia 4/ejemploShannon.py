import libguia4 as lib

alfabetoFuente = ["0","1"]
probs = [0.75, 0.25]
cod1 = ["0","1"]
entropFuente = lib.getEntropBaseR(probs)
longMedia = lib.getLongMedia(probs, cod1)
rend1, redund1 = lib.getRendimientoRedundancia(probs, cod1)

print("Alfabeto de la fuente: " + str(alfabetoFuente))
print("Probabilidades de la fuente: " + str(probs))
print("Entropía de la fuente: " + str(entropFuente))
print("Código utilizado (trivial): " + str(cod1))
print("Longitud media del código: " + str(longMedia))
print("Rendimiento del código: " + str(rend1))
print("")

ext2, probsExt2 = lib.getExtensionProbsOrdN(alfabetoFuente, probs, 2)
entropExt2 = lib.getEntropBaseR(probsExt2)
codExt2 = lib.getCodigoHuffman(ext2, probsExt2)
longExt2 = lib.getLongMedia(probsExt2, ext2)
rend2, redund2 = lib.getRendimientoRedundancia(probsExt2, codExt2)

print("Alfabeto de la fuente: " + str(ext2))
print("Probabilidades de la fuente: " + str(probsExt2))
print("Entropía de la fuente: " + str(entropExt2))
print("Código utilizado (obtenido por Huffman): " + str(codExt2))
print("Longitud media del código: " + str(longExt2))
print("Rendimiento del código: " + str(rend2))
print("")