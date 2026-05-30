# relatorio.py

import base64
import os
from io import BytesIO

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_RELATORIO = os.path.join(PASTA, "relatorio.html")

NOMES = {
    "Run": "Corrida",
    "WeightTraining": "Musculação",
    "Ride": "Bicicleta",
}

CORES = {
    "Run": "#2ecc71",
    "WeightTraining": "#e74c3c",
    "Ride": "#3498db",
}

PRs = [
    {
        "distancias": ["5km"],
        "id": 14122176118,
        "faixa_km": (4.5, 6.0),
    },
    {
        "distancias": ["10km"],
        "id": 14091694123,
        "faixa_km": (9.0, 11.0),
    },
    {
        "distancias": ["15km", "21km | mesmo treino"],
        "id": 18078418890,
        "faixa_km": (14.0, 22.5),
    },
]


def achatar_dados(dados):
    """
    Transforma a lista de atividades numa lista plana de scrobbles,
    cada um com o tipo e nome da atividade associada.
    """
    linhas = []
    for atividade in dados:
        for musica in atividade["musicas"]:
            linhas.append({
                "tipo":        atividade["tipo"],
                "nome_treino": atividade["nome"],
                "inicio_ts":   atividade["inicio_ts"],
                "distancia_m": atividade["distancia_m"],
                "duracao_s":   atividade["duracao_s"],
                "artist":      musica["artist"],
                "track":       musica["track"],
                "album":       musica["album"],
            })
    return pd.DataFrame(linhas)


def grafico_barras(series, titulo, cor):
    """Gera um gráfico de barras horizontal e retorna como base64."""
    fig, ax = plt.subplots(figsize=(10, 5))
    series.sort_values().plot(kind="barh", ax=ax, color=cor)
    ax.set_title(titulo, fontsize=14)
    ax.set_xlabel("Plays")
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f'<img src="data:image/png;base64,{img}" style="width:60%; display:block;">'


def secao_tipo(df, tipo):
    """Gera o HTML de análise pra um tipo de atividade."""
    df_tipo = df[df["tipo"] == tipo]

    if df_tipo.empty:
        return f"<p>Nenhum dado encontrado para {NOMES[tipo]}.</p>"

    total_musicas = len(df_tipo)
    total_treinos = df_tipo["nome_treino"].count()
    cor = CORES[tipo]

    top_artistas = df_tipo["artist"].value_counts().head(10)
    top_musicas  = (df_tipo["artist"] + " — " + df_tipo["track"]).value_counts().head(10)
    top_albums   = df_tipo[df_tipo["album"] != ""]["album"].value_counts().head(10)

    grafico_art = grafico_barras(top_artistas, f"Top 10 Artistas — {NOMES[tipo]}", cor)
    grafico_alb = grafico_barras(top_albums,   f"Top 10 Álbuns — {NOMES[tipo]}", cor)

    tabela_musicas = pd.DataFrame({
        "Música": top_musicas.index,
        "Plays":  top_musicas.values,
    }).to_html(index=False, classes="tabela")

    return f"""
    <h2>{NOMES[tipo]}</h2>
    <p>{total_musicas:,} músicas em {total_treinos:,} treinos</p>
    {grafico_art}
    {grafico_alb}
    <h3>Top 10 Músicas</h3>
    {tabela_musicas}
    """


def secao_prs(dados):
    """Gera a seção de PRs com as músicas de cada recorde."""
    html = "<h2>Músicas nos meus melhores tempos</h2>"

    atividades_por_id = {a["id"]: a for a in dados}

    for pr in PRs:
        label = " + ".join(pr["distancias"])
        atividade = atividades_por_id.get(pr["id"])

        if not atividade:
            html += f"<p>⚠️ Atividade de {label} não encontrada nos dados.</p>"
            continue

        total_s      = atividade["duracao_s"]
        horas        = total_s // 3600
        minutos      = (total_s % 3600) // 60
        segundos     = total_s % 60
        if horas > 0:
            tempo_fmt = f"{horas}h {minutos:02d}min {segundos:02d}s"
        else:
            tempo_fmt = f"{minutos}min {segundos:02d}s"

        distancia_km = atividade["distancia_m"] / 1000
        pace_min_km  = (total_s / 60) / distancia_km
        pace_min     = int(pace_min_km)
        pace_seg     = int((pace_min_km - pace_min) * 60)
        pace_fmt     = f"{pace_min}:{pace_seg:02d} min/km"

        musicas = atividade["musicas"]

        if musicas:
            lista_musicas = "".join(
                f"<tr><td>{i+1}</td><td>{m['artist']}</td><td>{m['track']}</td><td>{m['album']}</td></tr>"
                for i, m in enumerate(musicas)
            )
            tabela = f"""
            <table class="tabela">
                <tr><th>#</th><th>Artista</th><th>Música</th><th>Álbum</th></tr>
                {lista_musicas}
            </table>
            """
        else:
            tabela = "<p>Nenhuma música registrada neste treino.</p>"

        html += f"""
        <h3>{label}</h3>
        <p>
            {atividade['nome']} &nbsp;|&nbsp;
            {distancia_km:.2f} km &nbsp;|&nbsp;
            {tempo_fmt} &nbsp;|&nbsp;
            {pace_fmt}
        </p>
	<details>
	    <summary>Ver {len(musicas)} músicas</summary>
            {tabela}
	</details>
        """

    return html


def gerar_relatorio(dados):
    """Gera o arquivo relatorio.html completo."""
    print("Gerando relatório...")

    df = achatar_dados(dados)

    css = """
    <style>
        body { font-family: Times New Roman, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; }
        h1 { color: #222; border-bottom: 3px solid #eee; padding-bottom: 10px; }
        h2 { color: #444; margin-top: 50px; border-bottom: 2px solid #eee; padding-bottom: 8px; }
        h3 { color: #555; margin-top: 30px; }
        .tabela { border-collapse: collapse; width: 100%; margin: 20px 0; }
        .tabela th, .tabela td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
        .tabela th { background-color: #f5f5f5; font-weight: bold; }
        .tabela tr:nth-child(even) { background-color: #fafafa; }
        img { border-radius: 8px; margin: 10px 0; }
    </style>
    """

    corpo = f"""
    <h1>Músicas nos meus treinos</h1>
    <p>Gerado em: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
    {secao_tipo(df, 'Run')}
    {secao_prs(dados)}
    {secao_tipo(df, 'WeightTraining')}
    {secao_tipo(df, 'Ride')}
    """

    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{corpo}</body></html>"

    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Relatório salvo em {ARQUIVO_RELATORIO}")
    print("  Abre o arquivo no navegador pra ver o resultado!")