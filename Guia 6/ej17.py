import libguia6 as lib

canalA = [[0, 1, 0],
          [0, 0, 1],
          [1, 0, 0],
          [1, 0, 0]]
sinRuidoA = lib.esCanalSinRuido(canalA)
determinanteA = lib.esCanalDeterminante(canalA)

print("El Canal A es sin ruido" if sinRuidoA else "El Canal A es con ruido")
print("El Canal A es determinante" if determinanteA else "El Canal A no es determinante")
print("Su ruido es de " + str(lib.getEntropPosterioriMediaBaseR(canalA, [0.25, 0.25, 0.25, 0.25])))
print("Su pérdida es de " + str(lib.getPerdidaTotalBaseR(canalA, [0.25, 0.25, 0.25, 0.25])))
print("")

canalB = [[1, 0, 0, 0],
          [0, 0.2, 0, 0.8],
          [0, 0, 1, 0]]
probsB = [1/3, 1/3, 1/3]

sinRuidoB = lib.esCanalSinRuido(canalB)
determinanteB = lib.esCanalDeterminante(canalB)


print("El Canal B es sin ruido" if sinRuidoB else "El Canal B es con ruido")
print("El Canal B es determinante" if determinanteB else "El Canal B no es determinante")
print("Su ruido es de " + str(lib.getEntropPosterioriMediaBaseR(canalB, probsB)))
print("Su pérdida es de " + str(lib.getPerdidaTotalBaseR(canalB, probsB)))
print("")

canalC = [[0.3, 0.5, 0.2],
          [0.2, 0.3, 0.5],
          [0.5, 0.2, 0.5]]
probsC = [1/3, 1/3, 1/3]

sinRuidoC = lib.esCanalSinRuido(canalC)
determinanteC = lib.esCanalDeterminante(canalC)

print("El Canal C es sin ruido" if sinRuidoC else "El Canal C es con ruido")
print("El Canal C es determinante" if determinanteC else "El Canal C no es determinante")
print("Su ruido es de " + str(lib.getEntropPosterioriMediaBaseR(canalC, probsC)))
print("Su pérdida es de " + str(lib.getPerdidaTotalBaseR(canalC, probsC)))
print("")

canalD = [[0, 0, 1, 0],
          [1, 0, 0, 0],
          [0, 1, 0, 0],
           [0, 0 ,0 ,1]]
probsD = [0.25] * 4

sinRuidoD = lib.esCanalSinRuido(canalD)
determinanteD= lib.esCanalDeterminante(canalD)

print("El Canal D es sin ruido" if sinRuidoD else "El Canal D es con ruido")
print("El Canal D es determinante" if determinanteD else "El Canal D no es determinante")
print("Su ruido es de " + str(lib.getEntropPosterioriMediaBaseR(canalD, probsD)))
print("Su pérdida es de " + str(lib.getPerdidaTotalBaseR(canalD, probsD)))
print("")