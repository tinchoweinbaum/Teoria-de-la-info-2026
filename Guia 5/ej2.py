import libguia5 as lib

mensajeA = "ABCDABCBDCBAAABBBCBCBABADBCBABCBDBCCCAAABB"
mensajeB = "AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO"

alfA, probsA = lib.getAlfabetoProbabilidades_mensaje(mensajeA)
alfB, probsB = lib.getAlfabetoProbabilidades_mensaje(mensajeB)

huffmanA, ShannonFanoA = lib.getCodigoHuffman(alfA, probsA), lib.getCodigoShannonFano(probsA, alfA)
huffmanB, ShannonFanoB = lib.getCodigoHuffman(alfB, probsB), lib.getCodigoShannonFano(probsB, alfB)

print("Alfabeto A: " + str(alfA))
print("Probabilidades de A: " + str(probsA))
print("Huffman de A: " + str(huffmanA))
print("Shannon-Fano de A: " + str(ShannonFanoA))
print("")

print("Alfabeto B: " + str(alfB))
print("Probabilidades de B: " + str(probsB))
print("Huffman de B: " + str(huffmanB))
print("Shannon-Fano de B: " + str(ShannonFanoB))
