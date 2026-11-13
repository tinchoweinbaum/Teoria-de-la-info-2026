import libguia4 as lib

probs = [0.5, 0.2, 0.3]
alfabeto = ["A", "B", "C"]
codigo = ["11", "010", "00"]

rendimientoA, redundanciaA = lib.getRedundanciaRendimiento(probs, codigo)
print(rendimientoA, redundanciaA)
print("")

alfExt, probsExt2 = lib.getExtensionProbsOrdN(alfabeto, probs, 2) # Obtengo el alfabeto extendido

codExt2 = lib.getCodigoHuffman(probsExt2, alfExt) # El código de la extensión de orden 2 NO está relacionado con el código de la fuente sin extender.

rendExt2, redundExt2 = lib.getRedundanciaRendimiento(probsExt2, codExt2)
print(rendExt2, redundExt2)

# El código de la extensión de orden 2 es mucho mejor porque se acerca más al límite teórico de la long. media, por medio de trabajar con extensiones, nos 
# acercamos mucho más a este límite a costo de tener exponencialmente más símbolos.