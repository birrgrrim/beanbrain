# BeanBrain

A personal coffee tracking tool for coffee enthusiasts. Track your beans, grinder settings, and reviews — never forget what worked.

## Features

- **Coffee catalog** — store beans with roastery, origin, process, roast level, score, taste profile
- **Auto-fill from URL** — paste a MadHeads roastery link to auto-import all coffee details, image, and flavor descriptors
- **Grinder settings** — remember the right setting per coffee, with basket size tracking (14g/18g/25g)
- **Reviews** — one review per person per coffee (editable), rate with coffee bean icons, add taste descriptors
- **Roastery vs personal taste** — see what the roastery claims vs what you actually taste
- **Coffee availability** — mark coffees as "have it" or "out", available ones sorted to top
- **Person management** — maintain a taster list, no typos
- **Equipment CRUD** — manage grinders, espresso machines, brew methods, basket sizes with defaults
- **Bilingual** — full EN/UA interface with one-click language toggle
- **Search** — find coffees by name or roastery
- **Hand-drawn design** — custom coffee illustrations, bean rating system, warm parchment theme

## Tech Stack

- **Backend**: Python / FastAPI / SQLAlchemy / SQLite
- **Frontend**: SvelteKit / Tailwind CSS v4 / TypeScript
- **Package manager**: uv (Python), npm (Node)
- **Future**: LLM integration (Open WebUI + Telegram), roastery price monitoring

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+

### Setup

```bash
git clone <repo-url>
cd beanbrain

make setup-backend    # installs Python deps via uv
make setup-frontend   # installs Node deps via npm
```

### Running

```bash
make dev              # starts both backend + frontend

# Or separately:
make dev-backend      # API at http://localhost:8000
make dev-frontend     # UI at http://localhost:5173
```

### Testing

```bash
make test             # 29 backend tests (in-memory SQLite)
```

## API Documentation

Once the backend is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
beanbrain/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app with lifespan
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # SQLite engine & session
│   │   ├── seed.py        # Seed data (80+ descriptors, equipment)
│   │   ├── routers/       # API endpoints
│   │   └── scrapers/      # Roastery scrapers (MadHeads)
│   ├── tests/             # pytest with in-memory SQLite
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.ts         # Typed API client
│   │   │   ├── i18n.ts        # EN/UA translations
│   │   │   └── components/    # Svelte components
│   │   └── routes/            # SvelteKit pages
│   └── static/img/            # Hand-drawn illustrations
├── CLAUDE.md                  # AI assistant context
├── Makefile
└── README.md
```

## License

MIT
