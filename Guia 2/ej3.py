import libguia2

probs = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
print("La entropía de las probabilidades de un dado normal es: ")
print(libguia2.getEntropiaFuente_listaProbs(probs))

print("")

probs = [1/9, 1/6, 1/9, 1/9, 1/6, 1/3]
print("Probabilidades del dado cargado: " + str(probs))
print("La entropía de este dado es")
print(libguia2.getEntropiaFuente_listaProbs(probs))

# La respuesta está mal por 0.01, preguntar si eso vale para el parcial o como e