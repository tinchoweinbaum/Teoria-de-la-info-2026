import libguia5 as lib
print(lib.__file__)

probs = [0.385, 0.154, 0.128, 0.154, 0.179]
huffman = lib.getCodigoHuffman(probs)
shannonF = lib.getCodigoShannonFano(probs)
entrop = lib.getEntropBaseR(probs)

print("Probabilidades de la fuente: " + str(probs))
print("Entropía: " + str(entrop))
print("")

print("Código de Huffman: " + str(huffman))
print("Longitud media del código de Huffman: " + str(lib.getLongMedia(probs, huffman)))
print("Rendimiento del código de Huffman: " + str(lib.getRendimientoCodigo(huffman, probs)))
print("")

print("Código de Shannon-Fano: " + str(shannonF))
print("Longitud media del código de Shannon-Fano: " + str(lib.getLongMedia(probs, shannonF)))
print("Rendimiento del código de Shannon-Fano: " + str(lib.getRendimientoCodigo(shannonF, probs)))
