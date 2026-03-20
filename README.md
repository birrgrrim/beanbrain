# BeanBrain

[![CI](https://github.com/birrgrrim/beanbrain/actions/workflows/ci.yml/badge.svg)](https://github.com/birrgrrim/beanbrain/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/birrgrrim/beanbrain)](https://github.com/birrgrrim/beanbrain/releases)

A personal coffee tracking tool for coffee enthusiasts. Track your beans, grinder settings, and reviews — never forget what worked.

## Features

- **Coffee catalog** — store beans with roastery, origin, process, roast level, score, taste profile, prices
- **Auto-fill from URL** — paste a MadHeads roastery link to auto-import all details, image, descriptors, and prices
- **Refresh & batch refresh** — re-scrape individual coffees or all coffees from a roastery (polite 3s delays)
- **Grinder settings** — remember the right setting per coffee/grinder/brew setup combination
- **Reviews** — one review per person per coffee, rate with coffee bean icons, add taste descriptors
- **Roastery vs personal taste** — see what the roastery claims vs what you actually taste
- **Stock tracking** — independent "at home" and "in store" status, stock-priority sorting
- **Sidebar filters** — filter by origin, roastery, roast level, rating, descriptors, stock status
- **Sidebar sorting** — sort by date, rating, price, or name (with stock priority always applied)
- **Equipment management** — grinders (auto/manual), brew setups (espresso, pourover, etc.), defaults
- **Bilingual** — full EN/UA interface with one-click language toggle
- **Responsive** — desktop (sidebar + 2-column detail), tablet (compact), mobile (single-panel navigation)
- **Hand-drawn design** — custom coffee illustrations, bean-brain logo, warm parchment theme

## Tech Stack

- **Backend**: Python / FastAPI / SQLAlchemy / SQLite
- **Frontend**: SvelteKit (adapter-node) / Tailwind CSS v4 / TypeScript
- **Package manager**: uv (Python), npm (Node)
- **Deploy**: launchd + Caddy reverse proxy (macOS)

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 22+

### Setup

```bash
git clone https://github.com/birrgrrim/beanbrain.git
cd beanbrain

make setup-backend    # installs Python deps via uv
make setup-frontend   # installs Node deps via npm
```

### Running

```bash
make dev              # starts both backend + frontend

# Or separately:
make dev-backend      # API at http://localhost:8001
make dev-frontend     # UI at http://localhost:5173
```

### Testing

```bash
make test             # 70 backend tests (in-memory SQLite)
```

### Production Deploy

```bash
make release          # builds tarball with pre-built frontend
make prod-setup       # installs runtime deps only
make prod-start       # starts backend + frontend
```

See the Makefile for `prod-stop` and `prod-backup` targets.

## API Documentation

Once the backend is running:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
beanbrain/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app with lifespan, CORS
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # SQLite engine & session
│   │   ├── seed.py        # Seed data (80+ descriptors, 36 origins)
│   │   ├── routers/       # API endpoints
│   │   └── scrapers/      # Roastery scrapers (MadHeads)
│   ├── tests/             # pytest with in-memory SQLite
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.ts         # Typed API client
│   │   │   ├── i18n.ts        # EN/UA translations (~130 keys)
│   │   │   ├── refData.ts     # Cached reference data store
│   │   │   └── components/    # 21 Svelte components
│   │   └── routes/            # SvelteKit pages
│   └── static/img/            # Hand-drawn illustrations
├── CLAUDE.md                  # AI assistant context
├── Makefile                   # dev, test, release, prod targets
└── README.md
```

## License

MIT
