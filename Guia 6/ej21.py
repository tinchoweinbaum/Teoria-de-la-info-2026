import libguia6 as lib

canalA = [[0.4, 0.6, 0, 0],
          [0, 0, 0.5, 0.5],
          [0, 0, 0.7, 0.3]]
reducidoA = lib.reduceCanal(canalA)

print("Canal A: ")
for fila in canalA: print(fila)

print("Canal A reducido: ")
for fila in reducidoA: print(fila)
print("")

canalB = [[0.2, 0.3, 0.5],
          [0, 0, 1],
          [0, 0, 1]]
reducidoB = lib.reduceCanal(canalB)

print("Canal B: ")
for fila in canalB: print(fila)

print("Canal B reducido: ")
for fila in reducidoB: print(fila)
print("")

canalC = [[0.4, 0, 0.2, 0.4],
          [0.4, 0.3, 0.2, 0.1],
          [0, 0.3, 0, 0.7]]
reducidoC = lib.reduceCanal(canalC)

print("Canal C: ")
for fila in canalC: print(fila)

print("Canal C reducido: ")
for fila in reducidoC: print(fila)
print("")

canalD = [[0, 0.5, 0, 0.5],
          [0.8, 0, 0.2, 0],
          [0, 0.5, 0, 0.5],
          [0.8, 0, 0.2, 0]]
reducidoD = lib.reduceCanal(canalD)

print("Canal D: ")
for fila in canalD: print(fila)

print("Canal D reducido: ")
for fila in reducidoD: print(fila)
print("")
