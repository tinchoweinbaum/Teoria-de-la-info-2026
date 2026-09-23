import libguia2

mensajes = []

mensajeA = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."
mensajes.append(mensajeA)

mensajeB = "+-/+/-//-/*-/**-*---////-+--*+*/-----/--+/++--*/-+"
mensajes.append(mensajeB)

mensajeC = "]]]([[]))([(])]([]([([([)([([([[([))][([([[([)([(]"
mensajes.append(mensajeC)

mensajeD = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"
mensajes.append(mensajeD)

mensajeE = "-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//"
mensajes.append(mensajeE)

mensajeF = ")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])"
mensajes.append(mensajeF)

for mensaje in mensajes:
    print("Mensaje: " + mensaje)
    alf, matTrans = libguia2.getAlfabeto_MatTrans(mensaje)

    print("Alfabeto: " + str(alf))

    print("Matriz de transición obtenida: ")
    libguia2.printearFuente(matTrans)

    memoria = libguia2.esFuenteMemoria(matTrans)
    stringMemoria = "La fuente es de memoria" if memoria else "La fuente no es de memoria"
    print("Con una tolerancia de 0.03 " + stringMemoria)

    if not memoria:
        _, vectorProbs = libguia2.getAlfabetoProbabilidades_mensaje(mensaje)
        entrop = libguia2.getEntropiaFuente_listaProbs(vectorProbs)
    else:
        entrop = libguia2.getEntropiaMarkov(matTrans,libguia2.getVectorMarkov_analitico(matTrans))

    print("Su entropía es " + str(entrop))
    print("----------------------------------------------------------------------------------------")
    print("")