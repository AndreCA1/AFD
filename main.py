import AutomatoFD
import data
import minimizacao

#Teste Criacao AFD
afd = AutomatoFD.AFD('ab')

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

print(afd)

#Teste de cadeia
cadeia = 'aababb'

afd.limpaAfd()
parada = afd.move(cadeia)

if not afd.deuErro() and afd.estadoFinal(parada):
    print('Aceita cadeia "{}"'.format(cadeia))
else:
    print('Rejeita cadeia "{}"'.format(cadeia))

#Teste exportacao
data.exportXml(afd, 'testeExport.jff')

#Teste importação
afd1 = data.importXml("afd1.jff")
print(afd1)
afd2 = data.importXml("afd2.jff")
afd3 = data.importXml("afd3.jff")

#Teste minimizacao
afdMinimizado = minimizacao.minimiza(afd1)
print(afdMinimizado)
data.exportXml(afdMinimizado, 'testeMinimizado.jff')

#teste se são equivalentes
if minimizacao.equivalentes(afd3, afd2): print('Os automatos são equivalentes')
else: print('Os automatos não são equivalentes')