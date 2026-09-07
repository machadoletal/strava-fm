# StravaFM

***English** · [Português](README.pt-BR.md)*

An analysis of the music I listen to during my workouts, cross-referencing
**Last.fm scrobbles** with **Strava activities**.

The script pulls from both sources, matches each track to the workout that was
happening at that moment, and generates an HTML report with rankings by
activity type and the "setlists" of my personal records.

📊 **[View sample report](https://machadoletal.github.io/strava-fm/)**
(GitHub Pages · `docs/index.html`)

## How it works

1. **Strava** — downloads every running, weight-training and cycling activity
   (`strava.py`), refreshing the access token from the refresh token.
2. **Last.fm** — downloads every scrobble since the date of the oldest workout
   (`lastfm.py`), retrying on HTTP 500.
3. **Cross-referencing** — for each activity, selects the scrobbles whose
   timestamp falls within the workout's `[start, end]` window (`main.py`).
4. **Report** — builds the HTML with charts (matplotlib) and tables
   (`relatorio.py`).

Downloaded data is cached in `dados.json` (Git-ignored); subsequent runs reuse
that file instead of calling the APIs.

## Stack

- Python 3.10+
- [requests](https://pypi.org/project/requests/) — API calls
- [pandas](https://pandas.pydata.org/) — cross-referencing and aggregation
- [matplotlib](https://matplotlib.org/) — charts
- [python-dotenv](https://pypi.org/project/python-dotenv/) — loads `.env`

## Running locally

```bash
git clone https://github.com/machadoletal/strava-fm.git
cd strava-fm

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env   # fill in your credentials
python main.py
```

The report is generated at `docs/index.html`. Delete `dados.json` first to
force a fresh fetch from the APIs.

### Credentials

| Variable | Where to get it |
| --- | --- |
| `LASTFM_API_KEY`, `LASTFM_USERNAME` | <https://www.last.fm/api/account/create> |
| `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET` | <https://www.strava.com/settings/api> |
| `STRAVA_REFRESH_TOKEN` | Strava OAuth flow with the `activity:read_all` scope |

## Project layout

```
strava-fm/
├── main.py          # orchestration: fetch, cross-reference, trigger the report
├── strava.py        # Strava API client
├── lastfm.py        # Last.fm API client
├── relatorio.py     # HTML generation (charts + tables)
└── docs/
    └── index.html   # generated report (served by GitHub Pages)
```

## License

[MIT](LICENSE)
