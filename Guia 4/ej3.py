import libguia4 as lib

probs = [0.5, 0.2, 0.3]

cod = ["11", "010", "00"]
ext2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]

print("El código A cumple el primer teorema de Shannon" if lib.cumpleShannon(probs, cod) else "El código A no cumple el primer teorema de Shannon")
print("Su extensión de orden 2 cumple el primer teorema de Shannon" if lib.cumpleShannon_extOrdN(probs, ext2, 2) else "Su extensión de orden 2 no cumple el primer teorema de Shannon")