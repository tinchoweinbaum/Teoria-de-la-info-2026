import libguia5 as lib

alf = ["A", "B", "C", "D"]
probs = [0.26190476190476186, 0.4047619047619049, 0.23809523809523808, 0.09523809523809523]

print(lib.getHuffmanShannonFano(probs))
print(lib.getCodigoHuffman(alf,probs))