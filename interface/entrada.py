from datetime import datetime

from regras.config import LINHAS, PERFIS


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro até o usuário digitar um valor válido."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  Entrada inválida. Digite apenas números.")


def ler_horario():
    """Lê um horário HH:MM. Enter usa o horário atual. Retorna (hora, minuto)."""
    agora = datetime.now()
    while True:
        texto = input(f"Horário (HH:MM) ou Enter para agora [{agora:%H:%M}]: ").strip()
        if texto == "":
            return agora.hour, agora.minute
        try:
            partes = texto.split(":")
            if len(partes) != 2:
                raise ValueError
            hora = int(partes[0])
            minuto = int(partes[1])
            if 0 <= hora <= 23 and 0 <= minuto <= 59:
                return hora, minuto
            print("  Horário fora do intervalo válido.")
        except ValueError:
            print("  Formato inválido. Use HH:MM, por exemplo 07:45.")


def escolher_linha():
    """Mostra as linhas disponíveis e devolve o nome da linha escolhida."""
    nomes = tuple(LINHAS.keys())
    print("\nLinhas disponíveis:")
    for i, nome in enumerate(nomes, start=1):
        print(f"  {i} - {nome}")
    escolha = ler_inteiro("Escolha a linha: ", 1, len(nomes))
    return nomes[escolha - 1]


def escolher_estacao(linha, rotulo):
    """Mostra as estações da linha e devolve o índice da estação escolhida."""
    estacoes = LINHAS[linha]["estacoes"]
    print(f"\n{rotulo} ({linha}):")
    for i, nome in enumerate(estacoes, start=1):
        print(f"  {i:2d} - {nome}")
    escolha = ler_inteiro("Número da estação: ", 1, len(estacoes))
    return escolha - 1


def escolher_perfil():
    """Pergunta se alguém precisa de assento preferencial."""
    print("\nAlguém do grupo precisa de assento preferencial?")
    for numero, (nome, _) in PERFIS.items():
        print(f"  {numero} - {nome}")
    escolha = ler_inteiro("Escolha: ", 1, len(PERFIS))
    nome, categoria = PERFIS[escolha]
    return nome, categoria
