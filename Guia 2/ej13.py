import libguia2

matTrans = [[1/2, 1/2, 0],
            [1/3, 1/3, 1/3],
            [0, 1, 0]
            ]

print("Matriz de transición de la fuente de Markov: ")
print(matTrans)
print("")

vecEst = libguia2.getVectorMarkov_analitico(matTrans)
print("Se vector estacionario es: " + str(vecEst))
print("La entropía de la fuente es " + str(libguia2.getEntropiaMarkov(matTrans, vecEst)))