import libguia2

cadena = "BABCABCBCABABBCABABACBCABCBABCABCABCACACBACBABCAB"

print("La cadena es " + cadena)
print("")

alfabeto, matTrans = libguia2.getAlfabeto_MatTrans(cadena)
print("El alfabeto de la fuente es " + str(alfabeto) + " y su matriz de transición es: ")
libguia2.printearFuente(matTrans)

print("Nuevo mensaje simulado de la fuente con longitud 10: " + libguia2.simularMensaje(10,alfabeto,matTrans))
