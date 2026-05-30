# lastfm.py

import requests
import time

URL = "https://ws.audioscrobbler.com/2.0/"


def buscar_pagina(api_key, username, pagina, from_ts=None):
    """Busca uma página de scrobbles e retorna o JSON da resposta."""
    parametros = {
        "method": "user.getRecentTracks",
        "api_key": api_key,
        "user": username,
        "format": "json",
        "limit": 200,
        "page": pagina,
    }
    if from_ts:
        parametros["from"] = from_ts

    resposta = requests.get(URL, params=parametros, timeout=15)
    resposta.raise_for_status()
    return resposta.json()


def buscar_scrobbles(api_key, username, from_ts=None):
    """
    Busca scrobbles do usuário, página por página.
    Se from_ts for informado, busca apenas a partir daquela data.
    Retorna uma lista de dicionários com artist, track, album e timestamp.
    """
    scrobbles = []
    pagina = 1
    total_paginas = None

    while total_paginas is None or pagina <= total_paginas:
        print(f"  Buscando página {pagina} de {total_paginas or '?'}...")

        dados = buscar_pagina(api_key, username, pagina, from_ts)

        if total_paginas is None:
            total_paginas = int(dados["recenttracks"]["@attr"]["totalPages"])

        faixas = dados["recenttracks"].get("track", [])

        if isinstance(faixas, dict):
            faixas = [faixas]

        for faixa in faixas:
            if faixa.get("@attr", {}).get("nowplaying") == "true":
                continue

            timestamp = faixa.get("date", {}).get("uts")
            if not timestamp:
                continue

            scrobbles.append({
                "artist": faixa["artist"]["#text"],
                "track":  faixa["name"],
                "album":  faixa.get("album", {}).get("#text", ""),
                "timestamp": int(timestamp),
            })

        pagina += 1
        time.sleep(0.25)

    print(f"  Total: {len(scrobbles):,} scrobbles carregados.")
    return scrobbles