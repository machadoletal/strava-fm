# StravaFM

*[English](README.md) · **Português***

Análise das músicas que ouço durante meus treinos, cruzando os dados de
**scrobbles do Last.fm** com as **atividades do Strava**.

O script busca as duas fontes, casa cada música com o treino que estava
acontecendo naquele horário e gera um relatório HTML com rankings por tipo de
atividade e os "setlists" dos meus melhores tempos.

📊 **[Ver relatório de exemplo](https://machadoletal.github.io/strava-fm/)**
(GitHub Pages · `docs/index.html`)

## Como funciona

1. **Strava** — baixa todas as atividades de corrida, musculação e bicicleta
   (`strava.py`), renovando o access token a partir do refresh token.
2. **Last.fm** — baixa todos os scrobbles a partir da data do treino mais
   antigo (`lastfm.py`), com retry em caso de erro 500.
3. **Cruzamento** — para cada atividade, seleciona os scrobbles cujo timestamp
   cai dentro do intervalo `[início, fim]` do treino (`main.py`).
4. **Relatório** — monta o HTML com gráficos (matplotlib) e tabelas
   (`relatorio.py`).

Os dados baixados são guardados em `dados.json` (ignorado pelo Git); nas
próximas execuções o script reaproveita esse arquivo em vez de chamar as APIs.

## Stack

- Python 3.10+
- [requests](https://pypi.org/project/requests/) — chamadas às APIs
- [pandas](https://pandas.pydata.org/) — cruzamento e agregação
- [matplotlib](https://matplotlib.org/) — gráficos
- [python-dotenv](https://pypi.org/project/python-dotenv/) — carga do `.env`

## Rodando localmente

```bash
git clone https://github.com/machadoletal/strava-fm.git
cd strava-fm

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env   # preencha com suas credenciais
python main.py
```

O relatório é gerado em `docs/index.html`.

### Credenciais

| Variável | Onde obter |
| --- | --- |
| `LASTFM_API_KEY`, `LASTFM_USERNAME` | <https://www.last.fm/api/account/create> |
| `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET` | <https://www.strava.com/settings/api> |
| `STRAVA_REFRESH_TOKEN` | fluxo OAuth do Strava com escopo `activity:read_all` |

## Estrutura

```
strava-fm/
├── main.py          # orquestração: busca, cruza e dispara o relatório
├── strava.py        # cliente da API do Strava
├── lastfm.py        # cliente da API do Last.fm
├── relatorio.py     # geração do HTML (gráficos + tabelas)
└── docs/
    └── index.html   # relatório gerado (servido pelo GitHub Pages)
```

## Licença

[MIT](LICENSE)
