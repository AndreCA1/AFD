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

    #passa pelo campos em brancos verificando se algum de seus possiveis estados equivalentes está marcado
    for chave, valor in tabela.items():
        if isinstance(valor, list):
            for tupla in valor:
                if not isinstance(tabela[tupla], list):
                    tabela[chave] = tabela[tupla]
                    break

    #pega as tuplas e tranforma em conjuntos de estados equivalentes
    #usei busca em profundidade no grafo representado por lista de adjascencia
    grafo = {}
    for (a, b), valor in tabela.items():
        if not isinstance(valor, bool):
            grafo.setdefault(a, set()).add(b)
            grafo.setdefault(b, set()).add(a)

    #percorre os grupos conectados
    visitados = set()
    grupos = []

    def dfs(no, grupo):
        visitados.add(no)
        grupo.add(no)
        for vizinho in grafo.get(no, []):
            if vizinho not in visitados:
                dfs(vizinho, grupo)

    for no in grafo:
        if no not in visitados:
            grupo = set()
            dfs(no, grupo)
            grupos.append(sorted(grupo))

    return grupos

def minimiza(afd):
    afd.eColmpleto()
    transicoes = afd.transicoesPorEstado()
    novoAFD = data.copiaAFD(afd)

    inacessiveis = afd.estadosNaoConexos(transicoes)
    for id in inacessiveis:
        novoAFD.removeEstado(id)

    equivalentes = estadosEquivalentes(afd, transicoes)

    #Compara 1 estado com todos os outros
    for i in equivalentes:
        for j in i[1:]:
            #Passa por todas as transicoes
            for k in transicoes:
                for caminho, destino in transicoes[k]:
                        if destino == j:
                            if k != destino:
                                transicoes[k].remove((caminho, destino))
                                transicoes[k].append((caminho, i[0]))
                            else:
                                if (caminho, i[0]) not in transicoes[i[0]]:
                                    transicoes[i[0]].append((caminho, i[0]))
            novoAFD.removeEstado(j)

    #Limpa as antigas transicoes e coloca as novas
    novoAFD.transicoes = dict()
    for i in transicoes:
        for simbolo, destino in transicoes[i]:
            novoAFD.criaTransicao(i, destino, simbolo)

    return novoAFD

#refazer isso aq
def equivalentes(afd1, afd2):
    afd1 = minimiza(afd1)
    afd2 = minimiza(afd2)

    if afd1.alfabeto == afd2.alfabeto and len(afd1.transicoes) == len (afd2.transicoes):
        for x in afd1.transicoes:
            if x not in afd2.transicoes: return False
        return True
    return False