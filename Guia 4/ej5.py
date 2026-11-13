import libguia4 as lib

probs = [0.7, 0.3]
alfabeto = [0, 1]

ext2, probsExt2 = lib.getExtensionProbsOrdN(alfabeto, probs, 2)
print("Extensión de orden 2 de la fuente binaria: " + str(ext2))

huffmanExt2 = lib.getCodigoHuffman(probsExt2, ext2)
print("Extensión de orden 2 codificada con Huffman: " + str(huffmanExt2))
print("El código cumple el teorema de Shannon" if lib.cumpleShannon(probsExt2, ext2) else "El código no cumple el teorema de Shannon")