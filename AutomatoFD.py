from sqlalchemy.testing import fails_on_everything_except
from sympy import false


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

if __name__ == '__main__':
    afd = AutomatoFD('ab')

    for i in range (1,5):
        afd.criaEstado(i)
    afd.mudaEstadoInicial(1)
    afd.mudaEstadoFinal(4,True)

    afd.criaTransicao(1,2,'a')
    afd.criaTransicao(2,1,'a')
    afd.criaTransicao(3,4,'a')
    afd.criaTransicao(4,3,'a')
    afd.criaTransicao(1,3,'b')
    afd.criaTransicao(3,1,'b')
    afd.criaTransicao(2,4,'b')
    afd.criaTransicao(4,2,'b')

    print(afd)

    cadeia = 'abbabaabbbbbba'

    afd.limpaAfd()
    parada = afd.move(cadeia)

    if not afd.deuErro() and afd.estadoFinal(parada):
        print('Aceita cadeia "{}"'.format(cadeia))
    else:
        print('Rejeita cadeia "{}"'.format(cadeia))