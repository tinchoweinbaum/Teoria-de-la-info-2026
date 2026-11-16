import libguia6 as lib

canalA = [[0, 1, 0],
          [0, 0, 1],
          [1, 0, 0],
          [1, 0, 0]]
probsA = [0.25, 0.25, 0.25, 0.25]

canalB = [[1, 0, 0, 0],
          [0, 0.2, 0, 0.8],
          [0, 0, 1, 0]]
probsB = [1/3, 1/3, 1/3]

canalD = [[0, 0, 1, 0],
          [1, 0, 0, 0],
          [0, 1, 0, 0],
           [0, 0 ,0 ,1]]
probsD = [0.25] * 4

canales = [canalA, canalB, canalD]

for canal in canales:
    print("Canal: ")
    for fila in canal:
        print(fila)
    print("Capacidad del canal: " + str(lib.getCapacidadCanal(canal)))
    print("")