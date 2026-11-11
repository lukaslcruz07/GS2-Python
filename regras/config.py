"""
config.py - Constantes e dados fixos do LotaTrem.

Aqui ficam as linhas, estações, assentos e demais valores usados pelo sistema.
Se quiser adicionar uma linha ou mudar a quantidade de assentos, é só aqui.
"""

ARQUIVO_DADOS = "dados_lotatrem.json"
JANELA_MINUTOS = 60      # até quanto tempo à frente buscamos trens
LIMITE_CONFORTO = 70     # acima disso o trem é considerado desconfortável
INICIO_OPERACAO = 5      # 05h
FIM_OPERACAO = 24        # 00h

# Lotação base (%) para cada hora do dia (índice = hora, de 0 a 23)
CURVA_HORARIA = (
    5, 3, 2, 2, 5, 15, 45, 85, 95, 70, 45, 40,
    50, 50, 40, 42, 55, 80, 95, 90, 65, 40, 25, 12,
)

# Cada linha tem: intervalo entre trens (min), fator de lotação e estações
LINHAS = {
    "Linha 1-Azul": {
        "intervalo": 4,
        "fator": 1.0,
        "estacoes": (
            "Jabaquara", "Conceição", "São Judas", "Saúde", "Praça da Árvore",
            "Santa Cruz", "Vila Mariana", "Ana Rosa", "Paraíso", "Vergueiro",
            "São Joaquim", "Liberdade", "Sé", "São Bento", "Luz",
            "Tiradentes", "Armênia", "Portuguesa-Tietê", "Carandiru",
            "Santana", "Jd. São Paulo-Ayrton Senna", "Parada Inglesa",
            "Tucuruvi",
        ),
    },
    "Linha 2-Verde": {
        "intervalo": 5,
        "fator": 0.8,
        "estacoes": (
            "Vila Madalena", "Sumaré", "Clínica", "Consolação",
            "Trianon-Masp", "Brigadeiro", "Paraíso", "Ana Rosa",
            "Chácara Klabin", "Santos-Imigrantes", "Alto do Ipiranga",
            "Sacomã", "Tamanduateí", "Vila Prudente",
        ),
    },
    "Linha 3-Vermelha": {
        "intervalo": 3,
        "fator": 1.1,
        "estacoes": (
            "Palmeiras-Barra Funda", "Marechal Deodoro", "Santa Cecília",
            "República", "Anhangabaú", "Sé", "Pedro II", "Brás",
            "Bresser-Mooca", "Belém", "Tatuapé", "Carrão", "Penha",
            "Vila Matilde", "Guilhermina-Esperança", "Patriarca",
            "Artur Alvim", "Corinthians-Itaquera",
        ),
    },
}

# Estações de grande movimento (plataforma costuma ficar mais cheia)
ESTACOES_BALDEACAO = (
    "Sé", "República", "Paraíso", "Luz", "Brás", "Palmeiras-Barra Funda",
    "Ana Rosa", "Consolação", "Tatuapé",
)

# Assentos por trem (valores fictícios para a simulação)
ASSENTOS = {"comuns": 180, "Idosos": 24, "Gestantes": 12, "PcD": 12}

# Perfis de passageiro: número -> (nome, categoria de assento preferencial)
PERFIS = {
    1: ("Nenhum (assento comum)", None),
    2: ("Idoso", "Idosos"),
    3: ("Gestante", "Gestantes"),
    4: ("Pessoa com deficiência", "PcD"),
}

# Níveis para o usuário relatar a lotação: (nome, percentual)
NIVEIS_RELATO = (
    ("Tranquilo", 20),
    ("Moderado", 55),
    ("Cheio", 80),
    ("Superlotado", 95),
)
