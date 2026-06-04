# hltv-api

This project offers an easy-to-use interface for extracting [HLTV](https://www.hltv.org/) data through web scraping, providing a RESTful API built with FastAPI. With this tool, developers can easily pull HLTV data into their applications, websites, or data analysis workflows.

Please be aware that the deployed version is intended for testing purposes and includes rate limiting. For more flexibility and customization, it's recommended to host the service on your own cloud infrastructure.

### API Swagger

https://hltv-json-api.fly.dev/

### Running Locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), if you haven't already.

```bash
git clone https://github.com/eupeutro/hltv-api.git
cd hltv-api
uv sync
uv run uvicorn app.main:app
```

Then open http://localhost:8000/

### Running via Docker Compose (recommended)

Includes the API and [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for Cloudflare bypass.

```bash
git clone https://github.com/eupeutro/hltv-api.git
cd hltv-api
docker compose up --build
```

Then open http://localhost:8000/

### Testing

Tests require the Docker Compose stack to be running (`docker compose up -d`) since they hit the live API, which in turn scrapes HLTV through FlareSolverr.

Install dev dependencies:

```bash
uv sync --group dev
```

Run all tests:

```bash
uv run pytest tests/
```

Run a specific file:

```bash
uv run pytest tests/test_players.py
uv run pytest tests/test_teams.py
uv run pytest tests/test_events.py
uv run pytest tests/test_ranking.py
uv run pytest tests/test_matches.py
```

Run a single test:

```bash
uv run pytest tests/test_players.py::test_get_player_stats
```

Run with verbose output:

```bash
uv run pytest tests/ -v
```

Point tests at a different host (e.g. staging):

```bash
API_BASE_URL=http://my-host:8000 uv run pytest tests/
```

### Running via Docker (standalone)

```bash
git clone https://github.com/eupeutro/hltv-api.git
cd hltv-api
docker build -t hltv-api .
docker run -d -p 8000:8000 hltv-api
```

### Environment Variables

| Variable                  | Description                                                                                            | Default                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------- |
| `RATE_LIMITING_ENABLE`    | Enable rate limiting for API calls                                                                     | `false`                    |
| `RATE_LIMITING_FREQUENCY` | Delay allowed between each API call. See [slowapi](https://slowapi.readthedocs.io/en/latest/) for more | `2/3seconds`               |
| `FLARESOLVERR_URL`        | FlareSolverr instance URL for Cloudflare bypass                                                        | `http://localhost:8191/v1` |

Create a `.env` file in the project root to override defaults:

```
RATE_LIMITING_ENABLE=false
RATE_LIMITING_FREQUENCY=2/3seconds
FLARESOLVERR_URL=http://localhost:8191/v1
```

### Coverage

Tracks which [HLTV.org](https://www.hltv.org/) sections and features are implemented.

#### [News](https://www.hltv.org/news)

<details>
<summary>0% implemented (0/2)</summary>

- [ ] Latest news
- [ ] News article

</details>

#### [Matches](https://www.hltv.org/matches)

<details>
<summary>75% implemented (3/4)</summary>

- [x] Live matches
- [x] Today's matches (with timezone support)
- [x] Match stats
- [ ] Match details / scoreboard

</details>

#### [Results](https://www.hltv.org/results)

<details>
<summary>0% implemented (0/1)</summary>

- [ ] Results list

</details>

#### [Events](https://www.hltv.org/events)

<details>
<summary>67% implemented (4/6)</summary>

- [x] Search events
- [x] Event profile (overview)
- [x] Event team stats
- [x] Event results
- [ ] Event player stats
- [ ] Event maps stats

</details>

#### [Players](https://www.hltv.org/stats/players)

<details>
<summary>78% implemented (7/9)</summary>

- [x] Search players
- [x] Player profile
- [x] Player stats
- [x] Player career stats
- [x] Player trophies
- [x] Player team achievements
- [x] Player personal achievements
- [ ] Player matches history
- [ ] Player news

</details>

#### [Teams](https://www.hltv.org/stats/teams)

<details>
<summary>63% implemented (5/8)</summary>

- [x] Search teams
- [x] Team profile
- [x] Team achievements
- [x] Team upcoming matches
- [x] Team results
- [ ] Team stats
- [ ] Team maps stats
- [ ] Team player stats

</details>

#### [Rankings](https://www.hltv.org/ranking/teams)

<details>
<summary>25% implemented (1/4)</summary>

- [x] World team ranking
- [ ] Regional rankings
- [ ] Valve ranking
- [ ] Player ranking

</details>

#### [Stats](https://www.hltv.org/stats)

<details>
<summary>0% implemented (0/7)</summary>

- [ ] Top players overview
- [ ] Top teams overview
- [ ] Player stats leaderboard
- [ ] Team stats leaderboard
- [ ] Match stats
- [ ] Event stats
- [ ] Map stats

</details>
