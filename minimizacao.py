from copy import deepcopy

import AutomatoFD
import data

def verificaTerminaisNaoTerminais(finais, estado1, estado2):
    if estado1 in finais and estado2 not in finais:
        return True
    elif estado1 not in finais and estado2 in finais:
        return True
    else:
        return None

def estadosEquivalentes(afd, transicoesEstado):
    tabela = {}
    estados = list(afd.estados)
    equivalentes = set()

    #Cria apenas metade da tabela
    for i in range(len(estados)):
        for j in range(i + 1, len(estados)):
            #Usa os estados como chave no dicionario. Atribui True para marcado quando nao são equivalentes e None quando não são
            tabela[(estados[i], estados[j])] = verificaTerminaisNaoTerminais(afd.finais, estados[i], estados[j])

    #.items devolve chave e valor
    for (estado1, estado2), marcado in tabela.items():
        if marcado is None:
            for i in range(len(afd.alfabeto)):
                destino1 = transicoesEstado[estado1][i][1]
                destino2 = transicoesEstado[estado2][i][1]

                if destino1 != destino2:
                    if not (destino1, destino2) in tabela:
                        destino1, destino2 = destino2, destino1

                    #Se os destinos ja tiverem marcados, os estados atuais tambem são marcados como True
                    if isinstance(tabela[destino1, destino2], bool):
                        tabela[estado1, estado2] = True
                        break

                    #Verifica se aquela posição da tabela já é uma lista
                    elif isinstance(tabela[estado1, estado2], list):
                        tabela[estado1, estado2].append((destino1, destino2))
                    else:
                        tabela[estado1, estado2] = []
                        tabela[estado1, estado2].append((destino1, destino2))

    for chave, valor in tabela.items():
        if isinstance(valor, list):
            for tupla in valor:
                if not isinstance(tabela[tupla], list):
                    tabela[chave] = tabela[tupla]
                    break

    for chave, valor in tabela.items():
        if not isinstance(valor, bool):
            equivalentes.add(chave)

    return equivalentes