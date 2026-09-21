import libguia2


alf = ["A", "B"]
probs = [0.8, 0.2]

extOrdN, probExtOrdN = libguia2.getExtensionProbsOrdN(alf, probs, 2)
print(extOrdN, probExtOrdN)