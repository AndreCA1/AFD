import AutomatoFD
import data


def multiplicacao(afd1: AutomatoFD.AFD, afd2: AutomatoFD.AFD):
    if afd1.alfabeto != afd2.alfabeto:
        raise ValueError("Autômatos com alfabetos diferentes")

    alfabeto = afd1.alfabeto
    novoAfd = AutomatoFD.AFD(alfabeto)

    id = 0
    idMap = {}

    #Cria os estados combinados e mapeia seus IDs em um dicionario
    for i in afd1.estados:
        for j in afd2.estados:
            novoAfd.criaEstado(id, False, False)
            idMap[(i, j)] = id
            id = id + 1

    inicial = idMap[(afd1.inicial, afd2.inicial)]
    novoAfd.mudaEstadoInicial(inicial)

    #Transições
    for (i, j), idEstado in idMap.items():
        for simbolo in alfabeto:
                dest1 = afd1.transicoes[(i,simbolo)]
                dest2 = afd2.transicoes[(j,simbolo)]
                destinoId = idMap[(dest1, dest2)]
                novoAfd.criaTransicao(idEstado, destinoId, simbolo)

    return novoAfd, idMap

def uniao(afd1: AutomatoFD.AFD, afd2: AutomatoFD.AFD):
    novoAFD, idMap = multiplicacao(afd1, afd2)

    for i in afd1.finais:
        for (estado1, estado2), id in idMap.items():
            if estado1 == i:
                novoAFD.mudaEstadoFinal(idMap[(estado1,estado2)], True)

    for i in afd2.finais:
        for (estado1, estado2), id in idMap.items():
            if estado2 == i:
                novoAFD.mudaEstadoFinal(idMap[(estado1,estado2)], True)

    return novoAFD

def intercecao(afd1: AutomatoFD.AFD, afd2: AutomatoFD.AFD):
    novoAFD, idMap = multiplicacao(afd1, afd2)

    for i in afd1.finais:
        for j in afd2.finais:
            novoAFD.mudaEstadoFinal(idMap[(i,j)], True)

    return novoAFD

#Aceita o primeiro e rejeita o segundo
def diferenca(afd1: AutomatoFD.AFD, afd2: AutomatoFD.AFD):
    novoAFD, idMap = multiplicacao(afd1, afd2)


    for i in afd1.finais:
        for j in afd2.estados:
            if j not in afd2.finais:
                novoAFD.mudaEstadoFinal(idMap[(i,j)], True)

    return novoAFD

def complemento(afd):
    novoAFD = data.copiaAFD(afd)

    for i in afd.estados:
        if i in afd.finais: novoAFD.mudaEstadoFinal(i, False)
        else: novoAFD.mudaEstadoFinal(i, True)

    return novoAFD