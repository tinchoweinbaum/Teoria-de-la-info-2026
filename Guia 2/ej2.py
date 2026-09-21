import libguia2

mensaje = ["A", "A", "C", "B", "B", "C", "A", "C"]
print("Dado el mensaje " + str(mensaje))
alfabeto, probabilidades = libguia2.getAlfabetoProbabilidades_mensaje(mensaje)
print("Su alfabeto es: " + str(alfabeto))
print("Su distribución de probabilidades es " + str(probabilidades))