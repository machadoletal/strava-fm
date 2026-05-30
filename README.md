# StravaFM

Análise das músicas que ouço durante meus treinos, cruzando dados do **Last.fm** e do **Strava**.

## O que o projeto faz

- Busca todos os meus scrobbles do Last.fm a partir da data do meu primeiro treino no Strava
- Busca todas as minhas atividades de corrida, musculação e bicicleta no Strava
- Cruza os dois: identifica quais músicas estavam tocando durante cada treino
- Gera um relatório HTML com análises por tipo de atividade e os setlists dos meus melhores tempos

## Tecnologias utilizadas

- Python
- [requests](https://pypi.org/project/requests/) — chamadas às APIs do Last.fm e Strava
- [pandas](https://pandas.pydata.org/) — cruzamento e análise dos dados
- [matplotlib](https://matplotlib.org/) — geração dos gráficos

## Como rodar

1. Clone o repositório
2. Instale as dependências:

python -m pip install requests pandas matplotlib python-dotenv

3. Crie um arquivo `.env` com suas credenciais:

LASTFM_API_KEY=...

LASTFM_USERNAME=...

STRAVA_CLIENT_ID=...

STRAVA_CLIENT_SECRET=...

STRAVA_REFRESH_TOKEN=...

4. Rode o script principal:

python main.py

5. Abra o arquivo `relatorio.html` gerado na pasta do projeto
