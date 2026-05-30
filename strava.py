# strava.py

import requests
import time
from datetime import datetime, timezone

URL_AUTH = "https://www.strava.com/oauth/token"
URL_API  = "https://www.strava.com/api/v3"

TIPOS_PERMITIDOS = {"Run", "WeightTraining", "Ride"}


def renovar_token(client_id, client_secret, refresh_token):
    """Troca o refresh token por um access token válido."""
    resposta = requests.post(URL_AUTH, data={
        "client_id":     client_id,
        "client_secret": client_secret,
        "grant_type":    "refresh_token",
        "refresh_token": refresh_token,
    }, timeout=15)
    resposta.raise_for_status()
    return resposta.json()["access_token"]


def buscar_atividades(client_id, client_secret, refresh_token):
    """
    Busca todas as atividades do Strava, filtrando apenas
    corrida, musculação e bicicleta.
    Retorna uma lista de dicionários.
    """
    access_token = renovar_token(client_id, client_secret, refresh_token)
    headers = {"Authorization": f"Bearer {access_token}"}

    atividades = []
    pagina = 1

    while True:
        print(f"  Buscando página {pagina} de atividades...")

        resposta = requests.get(
            f"{URL_API}/athlete/activities",
            headers=headers,
            params={"per_page": 200, "page": pagina},
            timeout=15,
        )
        resposta.raise_for_status()
        lote = resposta.json()

        if not lote:
            break

        for atividade in lote:
            tipo = atividade.get("sport_type", atividade.get("type", ""))

            if tipo not in TIPOS_PERMITIDOS:
                continue

            inicio = datetime.fromisoformat(
                atividade["start_date"].replace("Z", "+00:00")
            )
            inicio_ts = int(inicio.timestamp())
            duracao_s = int(atividade.get("elapsed_time", 0))

            atividades.append({
                "id":       atividade["id"],
                "nome":     atividade.get("name", ""),
                "tipo":     tipo,
                "inicio_ts": inicio_ts,
                "fim_ts":   inicio_ts + duracao_s,
                "duracao_s": duracao_s,
                "distancia_m": float(atividade.get("distance", 0)),
            })

        if len(lote) < 200:
            break

        pagina += 1
        time.sleep(0.5)

    print(f"  Total: {len(atividades)} atividades carregadas.")
    return atividades