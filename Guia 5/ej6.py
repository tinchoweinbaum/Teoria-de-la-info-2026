import libguia5 as lib

probs = [0.3, 0.1, 0.4, 0.5]
alfabeto = ["S1", "S2", "S3","S4"]
codigo = ["01", "10", "110","001"]

mensajeA = "S3S1S4S3S2S3S1S3S4S1"
codificadoA = lib.codificaMensajeCodigoBinario_bytearray(alfabeto, codigo, mensajeA)
print(codificadoA)

decodificadoA = lib.decodificaMensajeCodigoBinario_bytearray(alfabeto, codigo, codificadoA)
print(decodificadoA)