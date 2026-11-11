from interface.entrada import ler_inteiro
from interface.exibicao import exibir_menu, pausar
from interface.funcionalidades import (
    recomendar_horario, relatar_lotacao, ver_assentos_preferenciais,
    ver_historico, ver_lotacao,
)
from armazenamento.arquivo_json import carregar_dados


def main():
    dados = carregar_dados()
    print("Bem-vindo ao LotaTrem!")

    while True:
        exibir_menu()
        opcao = ler_inteiro("\nEscolha uma opção: ", 0, 5)

        match opcao:
            case 1:
                recomendar_horario(dados)
                pausar()
            case 2:
                ver_lotacao(dados)
                pausar()
            case 3:
                ver_assentos_preferenciais(dados)
                pausar()
            case 4:
                relatar_lotacao(dados)
                pausar()
            case 5:
                ver_historico(dados)
                pausar()
            case 0:
                print("\nObrigado por usar o LotaTrem. Boa viagem!")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma encerrado pelo usuário.")
