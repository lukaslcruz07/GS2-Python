"""
exibicao.py - Funções que apenas mostram informações na tela.
"""

from regras.calculos import classificar_lotacao, minutos_para_texto


def titulo(texto):
    print("\n" + "=" * 56)
    print(texto.center(56))
    print("=" * 56)


def barra_lotacao(percentual):
    """Barra visual simples, ex.: [#####-----]  50%."""
    cheios = percentual // 10
    return "[" + "#" * cheios + "-" * (10 - cheios) + f"] {percentual:3d}%"


def mostrar_trem(avaliacao):
    """Imprime horário, lotação e assentos livres de um trem."""
    livres = avaliacao["livres"]
    horario = minutos_para_texto(avaliacao["minutos"])
    nivel = classificar_lotacao(avaliacao["lotacao"])
    print(f"  {horario}  {barra_lotacao(avaliacao['lotacao'])}  {nivel}")
    print(
        f"         Assentos livres: {livres['comuns']} comuns | "
        f"{livres['Idosos']} idosos | {livres['Gestantes']} gestantes | "
        f"{livres['PcD']} PcD"
    )


def pausar():
    input("\nPressione Enter para voltar ao menu...")


def exibir_menu():
    titulo("LOTATREM - VIAJE COM CONFORTO")
    print("  1 - Recomendar melhor horário para viajar")
    print("  2 - Ver lotação da estação e dos próximos trens")
    print("  3 - Ver assentos preferenciais disponíveis")
    print("  4 - Relatar lotação (ajuda outros passageiros)")
    print("  5 - Ver histórico de consultas")
    print("  0 - Sair")
