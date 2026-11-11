"""
calculos.py - Regras do sistema: lotação, assentos e avaliação dos trens.

Os dados de lotação são SIMULADOS a partir de uma curva de horário de pico,
combinada com os relatos feitos pelos próprios usuários.
"""

from datetime import datetime

from regras.config import (
    ASSENTOS, CURVA_HORARIA, ESTACOES_BALDEACAO, FIM_OPERACAO,
    INICIO_OPERACAO, LINHAS,
)


def minutos_para_texto(total_minutos):
    """Converte minutos desde meia-noite em 'HH:MM'."""
    return f"{total_minutos // 60:02d}:{total_minutos % 60:02d}"


def fora_do_horario(hora, minuto):
    """Retorna True se o horário estiver fora do funcionamento (05:00 às 00:00)."""
    return hora * 60 + minuto >= FIM_OPERACAO * 60 or hora < INICIO_OPERACAO


def calcular_lotacao(linha, hora, minuto, dados):
    """Estima a lotação (0 a 100%) do trem da linha no horário informado."""
    atual = CURVA_HORARIA[hora]
    proxima = CURVA_HORARIA[(hora + 1) % 24]
    base = atual + (proxima - atual) * minuto / 60   # suaviza entre as horas
    base = base * LINHAS[linha]["fator"]

    if datetime.now().weekday() >= 5:                # fim de semana é mais vazio
        base = base * 0.6

    # pequena variação fixa para cada trem não ter exatamente o mesmo valor
    base = base + ((hora * 60 + minuto) * 7 + len(linha) * 3) % 11 - 5

    # relatos dos usuários para essa linha e hora ajustam a estimativa
    niveis = []
    for relato in dados["relatos"]:
        if relato["linha"] == linha and relato["hora"] == hora:
            niveis.append(relato["nivel"])
    if len(niveis) > 0:
        media = sum(niveis) / len(niveis)
        base = (base + media) / 2

    return max(0, min(100, round(base)))


def calcular_lotacao_estacao(linha, estacao, hora, minuto, dados):
    """A plataforma de estações de baldeação costuma ter mais gente."""
    percentual = calcular_lotacao(linha, hora, minuto, dados)
    if estacao in ESTACOES_BALDEACAO:
        percentual += 10
    return min(100, percentual)


def classificar_lotacao(percentual):
    """Transforma o percentual em um nível de lotação em texto."""
    if percentual <= 40:
        return "Tranquilo"
    elif percentual <= 70:
        return "Moderado"
    elif percentual <= 90:
        return "Cheio"
    else:
        return "Superlotado"


def calcular_assentos(percentual):
    """Devolve um dicionário com os assentos livres de cada tipo."""
    livres = {}
    for tipo, total in ASSENTOS.items():
        # assentos comuns enchem primeiro; os preferenciais, mais tarde
        limiar = 60 if tipo == "comuns" else 90
        ocupados = round(total * min(1, percentual / limiar))
        livres[tipo] = total - ocupados
    return livres


def proximas_partidas(hora, minuto, intervalo, janela):
    """Lista os horários (em minutos desde 00:00) dos trens na janela de tempo."""
    inicio = hora * 60 + minuto
    primeira = inicio + (intervalo - inicio % intervalo) % intervalo
    partidas = []
    for t in range(primeira, inicio + janela + 1, intervalo):
        if INICIO_OPERACAO * 60 <= t < FIM_OPERACAO * 60:
            partidas.append(t)
    return partidas


def avaliar_trem(linha, t, inicio, pessoas, categoria, dados):
    """Calcula lotação, assentos e pontuação (menor = melhor) de um trem."""
    lotacao = calcular_lotacao(linha, t // 60, t % 60, dados)
    livres = calcular_assentos(lotacao)

    if categoria is None:
        tem_assento = livres["comuns"] >= pessoas
    else:
        # uma pessoa usa o preferencial e as demais sentam nos comuns
        tem_assento = livres[categoria] >= 1 and livres["comuns"] >= pessoas - 1

    espera = t - inicio
    return {
        "minutos": t,
        "espera": espera,
        "lotacao": lotacao,
        "livres": livres,
        "tem_assento": tem_assento,
        "pontuacao": lotacao + espera * 0.5,   # esperar pouco também conta
    }


def pegar_pontuacao(avaliacao):
    """Função auxiliar usada para ordenar os trens pela pontuação."""
    return avaliacao["pontuacao"]
