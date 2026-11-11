"""
funcionalidades.py - As opções do menu do LotaTrem.

Cada função aqui corresponde a uma opção que o usuário escolhe no menu.
"""

from datetime import datetime

from regras.calculos import (
    avaliar_trem, calcular_lotacao_estacao, classificar_lotacao,
    fora_do_horario, minutos_para_texto, pegar_pontuacao, proximas_partidas,
)
from regras.config import ASSENTOS, JANELA_MINUTOS, LIMITE_CONFORTO, LINHAS, NIVEIS_RELATO
from interface.entrada import (
    escolher_estacao, escolher_linha, escolher_perfil, ler_horario, ler_inteiro,
)
from interface.exibicao import barra_lotacao, mostrar_trem, titulo
from armazenamento.arquivo_json import salvar_dados


def recomendar_horario(dados):
    titulo("MELHOR HORÁRIO PARA VIAJAR")
    linha = escolher_linha()
    estacoes = LINHAS[linha]["estacoes"]

    origem = escolher_estacao(linha, "Estação de ORIGEM")
    while True:
        destino = escolher_estacao(linha, "Estação de DESTINO")
        if destino != origem:
            break
        print("  Origem e destino devem ser diferentes.")

    pessoas = ler_inteiro("\nQuantas pessoas vão viajar juntas (1 a 10)? ", 1, 10)
    nome_perfil, categoria = escolher_perfil()
    hora, minuto = ler_horario()

    if fora_do_horario(hora, minuto):
        print("\nO sistema opera das 05:00 às 00:00. Tente um horário dentro desse período.")
        return

    inicio = hora * 60 + minuto
    sentido = estacoes[-1] if destino > origem else estacoes[0]
    avaliacoes = []
    for t in proximas_partidas(hora, minuto, LINHAS[linha]["intervalo"], JANELA_MINUTOS):
        avaliacoes.append(avaliar_trem(linha, t, inicio, pessoas, categoria, dados))

    if len(avaliacoes) == 0:
        print("\nNão há trens nessa janela de horário.")
        return

    confortaveis = []
    for av in avaliacoes:
        if av["lotacao"] <= LIMITE_CONFORTO and av["tem_assento"]:
            confortaveis.append(av)
    confortaveis.sort(key=pegar_pontuacao)

    print(f"\n{estacoes[origem]} -> {estacoes[destino]}  (sentido {sentido})")
    print(f"Grupo: {pessoas} pessoa(s) | Preferencial: {nome_perfil}")
    print("-" * 56)

    if len(confortaveis) > 0:
        melhor = confortaveis[0]
        print("MELHOR OPÇÃO:")
        mostrar_trem(melhor)
        if melhor["espera"] == 0:
            print("  -> Pode sair agora, o próximo trem já está confortável!")
        else:
            print(f"  -> Saia em {melhor['espera']} min para viajar com conforto.")
        if len(confortaveis) > 1:
            print("\nOUTRAS OPÇÕES:")
            for av in confortaveis[1:3]:
                mostrar_trem(av)
        horario_recomendado = minutos_para_texto(melhor["minutos"])
    else:
        avaliacoes.sort(key=pegar_pontuacao)
        print("Nenhum trem confortável (com assento para o grupo) na próxima hora.")
        print("O menos lotado no período é:")
        mostrar_trem(avaliacoes[0])
        print("  -> Considere sair em outro horário ou dividir o grupo.")
        horario_recomendado = minutos_para_texto(avaliacoes[0]["minutos"])

    dados["historico"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "linha": linha,
        "origem": estacoes[origem],
        "destino": estacoes[destino],
        "pessoas": pessoas,
        "horario_recomendado": horario_recomendado,
    })
    salvar_dados(dados)


def ver_lotacao(dados):
    titulo("LOTAÇÃO DA ESTAÇÃO E DOS TRENS")
    linha = escolher_linha()
    estacoes = LINHAS[linha]["estacoes"]
    indice = escolher_estacao(linha, "Estação")
    hora, minuto = ler_horario()

    if fora_do_horario(hora, minuto):
        print("\nO sistema opera das 05:00 às 00:00.")
        return

    plataforma = calcular_lotacao_estacao(linha, estacoes[indice], hora, minuto, dados)
    print(f"\nPlataforma de {estacoes[indice]}:")
    print(f"  {barra_lotacao(plataforma)}  {classificar_lotacao(plataforma)}")

    inicio = hora * 60 + minuto
    partidas = proximas_partidas(hora, minuto, LINHAS[linha]["intervalo"], JANELA_MINUTOS)
    print("\nPróximos trens:")
    for t in partidas[:4]:
        mostrar_trem(avaliar_trem(linha, t, inicio, 1, None, dados))


def ver_assentos_preferenciais(dados):
    titulo("ASSENTOS PREFERENCIAIS DISPONÍVEIS")
    linha = escolher_linha()
    hora, minuto = ler_horario()

    if fora_do_horario(hora, minuto):
        print("\nO sistema opera das 05:00 às 00:00.")
        return

    inicio = hora * 60 + minuto
    partidas = proximas_partidas(hora, minuto, LINHAS[linha]["intervalo"], JANELA_MINUTOS)
    print(f"\n{linha} - próximos trens:")
    for t in partidas[:3]:
        av = avaliar_trem(linha, t, inicio, 1, None, dados)
        print(f"\n  Trem das {minutos_para_texto(t)} (lotação {av['lotacao']}%)")
        for categoria in ("Idosos", "Gestantes", "PcD"):
            livres = av["livres"][categoria]
            total = ASSENTOS[categoria]
            if livres == 0:
                situacao = "ESGOTADO"
            elif livres <= 3:
                situacao = "POUCOS"
            else:
                situacao = "DISPONÍVEL"
            print(f"    {categoria:10s} {livres:2d}/{total:2d} livres  [{situacao}]")


def relatar_lotacao(dados):
    titulo("RELATAR LOTAÇÃO")
    linha = escolher_linha()
    estacoes = LINHAS[linha]["estacoes"]
    indice = escolher_estacao(linha, "Estação onde você está")
    hora, minuto = ler_horario()

    print("\nComo está a lotação agora?")
    for i, (nome, percentual) in enumerate(NIVEIS_RELATO, start=1):
        print(f"  {i} - {nome}")
    escolha = ler_inteiro("Escolha: ", 1, len(NIVEIS_RELATO))
    nome, percentual = NIVEIS_RELATO[escolha - 1]

    dados["relatos"].append({
        "linha": linha,
        "estacao": estacoes[indice],
        "hora": hora,
        "nivel": percentual,
    })
    if len(dados["relatos"]) > 200:      # mantém o arquivo pequeno
        dados["relatos"].pop(0)
    salvar_dados(dados)
    print(f"\nObrigado! Relato '{nome}' registrado para {estacoes[indice]} às {hora:02d}h.")


def ver_historico(dados):
    titulo("HISTÓRICO DE CONSULTAS")
    if len(dados["historico"]) == 0:
        print("Nenhuma consulta realizada ainda.")
        return
    for item in dados["historico"][-5:]:
        print(
            f"  {item['data']} | {item['linha']} | {item['origem']} -> "
            f"{item['destino']} | {item['pessoas']} pessoa(s) | "
            f"saída sugerida: {item['horario_recomendado']}"
        )
