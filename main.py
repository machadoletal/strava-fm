# main.py

import json
import os
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv

from lastfm import buscar_scrobbles
from strava import buscar_atividades

load_dotenv()

ARQUIVO_DADOS = "dados.json"


def carregar_dados_salvos():
    """Carrega dados do arquivo local, se existir."""
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def salvar_dados(dados):
    """Salva os dados processados em arquivo local."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"  Dados salvos em {ARQUIVO_DADOS}")


def cruzar_dados(atividades, scrobbles):
    """
    Para cada atividade, encontra os scrobbles que tocaram
    durante o intervalo [inicio_ts, fim_ts].
    Retorna uma lista de atividades enriquecidas com suas músicas.
    """
    resultado = []

    for atividade in atividades:
        musicas_do_treino = [
            s for s in scrobbles
            if atividade["inicio_ts"] <= s["timestamp"] <= atividade["fim_ts"]
        ]

        resultado.append({
            **atividade,
            "musicas": musicas_do_treino,
            "total_musicas": len(musicas_do_treino),
        })

    return resultado


def main():
    dados = carregar_dados_salvos()

    if dados:
        print("Dados encontrados localmente. Usando arquivo salvo.")
        print(f"  {len(dados)} atividades carregadas.")
    else:
        print("Nenhum dado salvo. Buscando das APIs...")

        print("\n[1/3] Buscando atividades do Strava...")
        atividades = buscar_atividades(
            client_id=os.getenv("STRAVA_CLIENT_ID"),
            client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
            refresh_token=os.getenv("STRAVA_REFRESH_TOKEN"),
        )

        # Pega a data do treino mais antigo pra filtrar o Last.fm
        inicio_mais_antigo = min(a["inicio_ts"] for a in atividades)
        data_formatada = datetime.fromtimestamp(inicio_mais_antigo, tz=timezone.utc)
        print(f"  Atividade mais antiga: {data_formatada.strftime('%d/%m/%Y')}")

        print("\n[2/3] Buscando scrobbles do Last.fm...")
        scrobbles = buscar_scrobbles(
            api_key=os.getenv("LASTFM_API_KEY"),
            username=os.getenv("LASTFM_USERNAME"),
            from_ts=inicio_mais_antigo,
        )

        print("\n[3/3] Cruzando dados...")
        dados = cruzar_dados(atividades, scrobbles)
        salvar_dados(dados)

    print(f"\nPronto! {len(dados)} atividades processadas.")
    return dados

if __name__ == "__main__":
    dados = main()
    from relatorio import gerar_relatorio
    gerar_relatorio(dados)