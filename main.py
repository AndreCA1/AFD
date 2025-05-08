import os
import data
import minimizacao
import multiplicacao


def nome_do_arquivo_sem_extensao(caminho):
    return os.path.splitext(os.path.basename(caminho))[0]

def main():
    afds = {}

    while True:
        print("\n=== MENU AFD ===")
        print("1. Importar AFD (XML)")
        print("2. Exportar AFD (XML)")
        print("3. Copiar AFD")
        print("4. Minimizar AFD")
        print("5. Testar equivalência entre dois AFDs")
        print("6. Operações com linguagens")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                caminho = data.escolher_arquivo_para_abrir()
                if caminho:
                    nome = nome_do_arquivo_sem_extensao(caminho)
                    afds[nome] = data.importXml(caminho)
                    print(f"AFD '{nome}' carregado com sucesso de '{caminho}'.")
                else:
                    print("Operação cancelada.")

            case '2':
                nome = input("Nome do AFD a ser exportado: ")
                if nome in afds:
                    caminho = data.escolher_arquivo_para_salvar()
                    if caminho:
                        data.exportXml(afds[nome], caminho)
                        print(f"AFD '{nome}' exportado com sucesso para '{caminho}'.")
                    else:
                        print("Operação cancelada.")
                else:
                    print("AFD não encontrado.")

            case '3':
                nome_original = input("Nome do AFD original: ")
                if nome_original in afds:
                    novo_nome = input("Nome para o novo AFD (cópia): ")
                    afds[novo_nome] = data.copiaAFD(afds[nome_original])
                    print(f"Cópia de '{nome_original}' criada como '{novo_nome}'.")
                else:
                    print("AFD original não encontrado.")

            case '4':
                caminho = data.escolher_arquivo_para_abrir()
                if caminho:
                    nome = nome_do_arquivo_sem_extensao(caminho)
                    afds[nome] = data.importXml(caminho)
                    if nome in afds:
                        nome_min = input("Nome para o AFD minimizado: ")
                        afds[nome_min] = minimizacao.minimiza(afds[nome])
                        data.exportXml(afds[nome_min], f"{nome_min}.jff")
                        print(f"AFD minimizado exportado como '{nome_min}'.")
                else:
                    print("Operação cancelada.")

            case '5':
                print("Selecione o primeiro AFD:")
                caminho1 = data.escolher_arquivo_para_abrir()
                print("Selecione o segundo AFD:")
                caminho2 = data.escolher_arquivo_para_abrir()
                if caminho1 and caminho2:
                    nome1 = nome_do_arquivo_sem_extensao(caminho1)
                    nome2 = nome_do_arquivo_sem_extensao(caminho2)

                    if nome1 not in afds:
                        afds[nome1] = data.importXml(caminho1)
                    if nome2 not in afds:
                        afds[nome2] = data.importXml(caminho2)

                    equivalentes = minimizacao.equivalentes(afds[nome1],afds[nome2])
                    print("AFDs equivalentes." if equivalentes else "AFDs diferentes.")
                else:
                    print("Operação cancelada.")

            case '6':
                print("\nOperações disponíveis:")
                print("a. União")
                print("b. Interseção")
                print("c. Complemento")
                print("d. Diferença")
                subop = input("Escolha a operação: ")

                if subop in {'a', 'b', 'd'}:
                    print("Selecione o primeiro AFD:")
                    caminho1 = data.escolher_arquivo_para_abrir()
                    print("Selecione o segundo AFD:")
                    caminho2 = data.escolher_arquivo_para_abrir()

                    if caminho1 and caminho2:
                        nome1 = nome_do_arquivo_sem_extensao(caminho1)
                        nome2 = nome_do_arquivo_sem_extensao(caminho2)
                        novo_nome = input("Nome para o AFD resultado: ")

                        if nome1 not in afds:
                            afds[nome1] = data.importXml(caminho1)
                        if nome2 not in afds:
                            afds[nome2] = data.importXml(caminho2)

                        match subop:
                            case 'a':
                                afds[novo_nome] = multiplicacao.uniao(afds[nome1], afds[nome2])
                                data.exportXml(afds[novo_nome], f"{novo_nome}.jff")
                            case 'b':
                                afds[novo_nome] = multiplicacao.intercecao(afds[nome1], afds[nome2])
                                data.exportXml(afds[novo_nome], f"{novo_nome}.jff")
                            case 'd':
                                afds[novo_nome] = multiplicacao.diferenca(afds[nome1], afds[nome2])
                                data.exportXml(afds[novo_nome], f"{novo_nome}.jff")
                        print(f"Operação realizada. Resultado salvo como '{novo_nome}'.")
                    else:
                        print("Operação cancelada.")

                elif subop == 'c':
                    caminho = data.escolher_arquivo_para_abrir()
                    if caminho:
                        nome = nome_do_arquivo_sem_extensao(caminho)
                        afds[nome] = data.importXml(caminho)

                        if nome not in afds:
                            afds[nome] = data.importXml(caminho)

                        novo_nome = input("Nome para o complemento: ")
                        afds[novo_nome] = multiplicacao.complemento(afds[nome])
                        data.exportXml(afds[novo_nome], f"{novo_nome}.jff")
                        print(f"Complemento salvo como '{novo_nome}'.")
                    else:
                        print("Operação cancelada.")
                else:
                    print("Operação inválida.")

            case '0':
                print("Encerrando.")
                break

            case _:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
