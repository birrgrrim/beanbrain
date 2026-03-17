# BeanBrain

A personal coffee tracking tool for coffee enthusiasts. Track your beans, grinder settings, and tastings — never forget what worked.

## Features

- **Coffee catalog** — store beans with roastery, origin, process, roast level
- **Grinder settings** — remember the right setting for each coffee
- **Tastings** — rate coffees (5-star with halves), add taste descriptors, compare notes with your partner
- **Roastery descriptors vs personal taste** — see what the roastery claims vs what you actually taste
- **Search by flavor** — find coffees by taste descriptors

## Tech Stack

- **Backend**: Python / FastAPI / SQLAlchemy / SQLite
- **Frontend**: SvelteKit / Tailwind CSS
- **Future**: LLM integration (Open WebUI + Telegram), roastery price scrapers

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+

### Setup

```bash
# Clone and enter
git clone <repo-url>
cd beanbrain

# Install backend dependencies
make setup-backend

# Install frontend dependencies
make setup-frontend
```

### Running

```bash
# Start both backend and frontend
make dev

# Or run them separately
make dev-backend   # API at http://localhost:8000
make dev-frontend  # UI at http://localhost:5173
```

### Testing

```bash
make test          # Run all tests
make test-backend  # Backend tests only
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
beanbrain/
├── backend/
│   ├── app/
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # DB connection & session
│   │   ├── seed.py        # Seed data (descriptors, equipment)
│   │   ├── main.py        # FastAPI app & startup
│   │   └── routers/       # API route handlers
│   ├── tests/             # pytest tests
│   └── pyproject.toml
├── frontend/              # SvelteKit app
├── Makefile
└── README.md
```

## License

MIT
