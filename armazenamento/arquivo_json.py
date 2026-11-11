import json

from regras.config import ARQUIVO_DADOS

def carregar_dados():
    dados_padrao = {"relatos": [], "historico": []}
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if "relatos" not in dados or "historico" not in dados:
            return dados_padrao
        return dados
    except FileNotFoundError:
        return dados_padrao
    except json.JSONDecodeError:
        print("Arquivo de dados corrompido. Começando com dados vazios.")
        return dados_padrao

def salvar_dados(dados):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except OSError:
        print("Não foi possível salvar os dados no arquivo.")
