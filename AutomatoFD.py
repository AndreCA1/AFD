import copy

from sympy import false
import xml.etree.ElementTree as ET


class AutomatoFD:

    #Funcao construtora
    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    def limpaAfd(self):
        #Cria essas variaveis e __ não deixa o usuario mexer nelas
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    def criaEstado(self, id, inicial = false, final = false):
        id = int(id)
        if id in self.estados:
            return False
        self.estados = self.estados.union({id})
        if inicial:
            self.inicial = id
        if final:
            self.finais = id
        return True

    def criaTransicao(self, origem, destino, simbolo):
        origem = int(origem)
        destino = int(destino)
        simbolo = str(simbolo)

        if not origem in self.estados:
            return False
        if not destino in self.estados:
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False
        self.transicoes[(origem, simbolo)] = destino
        return True

    def mudaEstadoInicial(self, id):
        if not id in self.estados:
            return False
        self.inicial = id

    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:
            return
        if final:
            #coloca no grupo dos finais
            self.finais = self.finais.union({id})
        else:
            #Tira do grupo dos finais
            self.finais = self.finais.difference({id})

    def move (self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                break
            #Caso exista um caminho do estado atual com o simbolo no conjunto de transicoes, o estado atual recebe eo novo estado
            if (self.__estadoAtual, simbolo) in self.transicoes.keys():
                self.__estadoAtual = self.transicoes[(self.__estadoAtual, simbolo)]
            else:
                self.__deuErro = True
                break
        return self.__estadoAtual

    def deuErro(self):
        return self.__deuErro

    def estadoAtual(self):
        return self.__estadoAtual

    #retorna true caso o ultimo estado apos processar a cadeia seja um estado final
    def estadoFinal(self, id):
        return id in self.finais

    #Toda vez que o python precisar enxergar a variavel como string ele vai chamar esse metodo (passa o afd pra str)
    def __str__(self):
        s = 'AFD(E, A, T, i, F): \n'
        s += '   E = { '
        for e in self.estados:
            s+= '{} '.format(str(e))
        s += '} \n'
        s += '   T = { '
        for (e,a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({}, '{}')-->{}, ".format(e, a, d)
        s += '} \n'
        s += '   i = {} \n'.format(self.inicial)
        s += '   F = { '

        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'

        return s

def importXml(caminho):

    #pega o arquivo e tranforma em uma arvore de elementos e pega seu no raiz
    raiz = ET.parse(str(caminho)).getroot()

    # Pegando o nó <automaton>
    automaton = raiz.find('automaton')

    alfabeto = set()

    for transicao in automaton.findall('transition'):
        alfabeto.add(transicao.find('read').text)

    alfabeto = ''.join(sorted(alfabeto))

    afd = AutomatoFD(alfabeto)

    for state in automaton.findall('state'):
        id = int(state.attrib['id'])
        afd.criaEstado(id)

        if not state.find('initial') == None:
            afd.mudaEstadoInicial(id)
        if not state.find('final') == None:
            afd.mudaEstadoFinal(id, True)

    for transicao in automaton.findall('transition'):
        afd.criaTransicao(transicao.find('from').text, transicao.find('to').text, transicao.find('read').text)
    return afd

def exportXml(afd, caminho):
    #criando estrutura do xml = ao gerado pelo jflap
    estrutura = ET.Element('structure')

    tipo = ET.SubElement(estrutura, 'type')
    tipo.text = 'fa'

    automato = ET.SubElement(estrutura, 'automaton')

    id_map = {}
    for idx, estado in enumerate(sorted(afd.estados)):
        #cria cada <state> passando id(idx(contador auxiliar)) e nome (q{valor do estado})
        estado_elem = ET.SubElement(automato, 'state', id=str(idx), name= 'q{}'.format(estado))
        id_map[estado] = str(idx)

        #seta posicao
        ET.SubElement(estado_elem, 'x').text = str(100 + 100 * idx)
        ET.SubElement(estado_elem, 'y').text = str(100)

        if estado == afd.inicial:
            ET.SubElement(estado_elem, 'initial')
        if estado in afd.finais:
            ET.SubElement(estado_elem, 'final')

    for (origem, simbolo), destino in afd.transicoes.items():
        transicao = ET.SubElement(automato, 'transition')
        ET.SubElement(transicao, 'from').text = id_map[origem]
        ET.SubElement(transicao, 'to').text = id_map[destino]
        ET.SubElement(transicao, 'read').text = simbolo

    tree = ET.ElementTree(estrutura)
    tree.write(caminho, encoding='utf-8', xml_declaration=True)
    print(f"Arquivo JFLAP exportado para: {caminho}")

def copiaAFD(afdOriginal):
    return copy.deepcopy(afdOriginal)

def transicoesPorEstado(afd):
    transicoesEstado = {}

    for (origem, simbolo), destino in afd.transicoes.items():
        if origem not in transicoesEstado:
            transicoesEstado[origem] = []
        transicoesEstado[origem].append((simbolo, destino))

    return transicoesEstado


def estadosEquivalentes(transicoesEstado):
    equivalentes = set()
    estadosOrdenados = sorted(transicoesEstado.keys())
    
    #passa por cada estado, de forma ordenada pelo ID
    for i in range(len(estadosOrdenados)):
        #compara o atual com os da frente Ex: 1 com 2,3,4 depois 2 com 3 e 4, etc
        for j in range(i + 1, len(estadosOrdenados)):
            estadoI = estadosOrdenados[i]
            estadoJ = estadosOrdenados[j]

            transacaoI = sorted(transicoesEstado.get(estadoI, []))
            transacaoJ = sorted(transicoesEstado.get(estadoJ, []))

            if transacaoI == transacaoJ:
                equivalentes.add((estadoI, estadoJ))

    print(equivalentes)



if __name__ == '__main__':
    afd = AutomatoFD('ab')

    for i in range (1,5):
        afd.criaEstado(i)
    afd.mudaEstadoInicial(1)
    afd.mudaEstadoFinal(4,True)

    afd.criaTransicao(1,2,'a')
    afd.criaTransicao(2,1,'a')
    afd.criaTransicao(3,2,'a')
    afd.criaTransicao(4,3,'a')
    afd.criaTransicao(1,3,'b')
    afd.criaTransicao(3,3,'b')
    afd.criaTransicao(2,4,'b')
    afd.criaTransicao(4,2,'b')

    # print(afd)
    # cadeia = 'abbabaabbbbbba'
    #
    # afd.limpaAfd()
    # parada = afd.move(cadeia)
    #
    # if not afd.deuErro() and afd.estadoFinal(parada):
    #     print('Aceita cadeia "{}"'.format(cadeia))
    # else:
    #     print('Rejeita cadeia "{}"'.format(cadeia))
    #
    # exportXml(afd, 'testeExport.jff')

    afd2 = importXml('testeImport.jff')
    # print(afd2)
    # afd3 = copiaAFD(afd)
    print(afd2)

    estadosEquivalentes(transicoesPorEstado(afd2))
