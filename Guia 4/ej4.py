import libguia4 as lib

probs = [0.8, 0.2]
alfabeto = [0, 1]

huffman = lib.getCodigoHuffman(probs, alfabeto)
print(huffman)