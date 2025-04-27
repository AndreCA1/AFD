import copy
import xml.etree.ElementTree as ET
import AutomatoFD

def importXml(caminho):

    #pega o arquivo e tranforma em uma arvore de elementos e pega seu no raiz
    raiz = ET.parse(str(caminho)).getroot()

    # Pegando o nó <automaton>
    automaton = raiz.find('automaton')

    alfabeto = set()

    for transicao in automaton.findall('transition'):
        text = transicao.find('read').text
        if text is None:
            raise ("Automato nao e deterministico")
        alfabeto.add(text)

    alfabeto = ''.join(sorted(alfabeto))

    afd = AutomatoFD.AFD(alfabeto)

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