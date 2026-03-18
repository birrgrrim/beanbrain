# CLAUDE.md — BeanBrain

## Project Overview
BeanBrain is a personal coffee tracking tool for managing coffee beans, grinder settings, and reviews. Built for local use on a Mac Mini.

## Stack
- **Backend**: Python 3.12+ / FastAPI / SQLAlchemy / SQLite
- **Frontend**: SvelteKit / Tailwind CSS v4 / TypeScript
- **Package manager**: uv (Python), npm (Node)
- **No Docker** — runs locally with `make dev`

## Running
```bash
make setup-backend    # uv sync
make setup-frontend   # npm install
make dev              # starts both (backend :8000, frontend :5173)
make test             # runs backend pytest
```

## Project Structure
```
backend/
  app/
    main.py           # FastAPI app with lifespan, CORS
    models.py         # SQLAlchemy models (Coffee, Review, Equipment, etc.)
    schemas.py        # Pydantic request/response schemas
    database.py       # SQLite engine + session
    seed.py           # Initial data (descriptors, equipment, baskets)
    routers/          # API endpoints (coffees, reviews, equipment, scrape, etc.)
    scrapers/         # Roastery scrapers (MadHeads implemented)
  tests/              # pytest with in-memory SQLite
frontend/
  src/
    app.css           # Tailwind + custom theme (parchment colors)
    lib/
      api.ts          # Typed API client
      i18n.ts         # EN/UA translations (~80 keys)
      lang.ts         # Language store (localStorage)
      components/     # Svelte components
    routes/
      +page.svelte    # Main SPA (sidebar + panel, tab switching)
      +layout.svelte  # Root layout (fonts, base styles)
  static/img/         # Hand-drawn illustrations (transparent PNGs)
```

## Key Design Decisions
- **One review per person per coffee** — upsert via PUT, not multiple tastings
- **Coffee availability** — `is_available` flag, sorted in sidebar, dimmed when out
- **Equipment defaults** — `is_default` on grinder/method/basket, used for sidebar display
- **MadHeads scraper** — parses SvelteKit embedded data from HTML, supports EN/UK
- **Bean rating** — hand-drawn coffee bean images (full/half/empty) replace star SVGs
- **18px base font** — optimized for Retina/HiDPI displays

## Design Language
- **Color**: Warm parchment palette (`#f4ecdd` bg, `#faf6ee` cards, amber accents)
- **Typography**: DM Serif Display (headings) + DM Sans (body)
- **Art**: Hand-drawn coffee illustrations, transparent PNGs, consistent sepia/brown style
- **Layout**: Sidebar (420px) + content panel, tab navigation (Coffee/Grinders/Persons)

## API Patterns
- Coffees: `GET/POST /coffees/`, `GET/PUT/DELETE /coffees/{id}`
- Reviews: `PUT /coffees/{id}/reviews/` (upsert), `DELETE /coffees/{id}/reviews/{rid}`
- Grinder settings: `POST/DELETE /coffees/{id}/settings/`
- Equipment CRUD: `GET/POST/PUT/DELETE /equipment`, `/brew-methods`, `/basket-sizes`
- Scrape: `GET /scrape/?url=...`
- Coffee list returns `avg_rating` and `default_grind` computed fields

## Testing
- Backend: pytest with in-memory SQLite (29 tests)
- Frontend: no tests yet
- Run: `cd backend && uv run pytest tests/ -v`

## Conventions
- Commits co-authored with Claude
- Ukrainian translations maintained alongside English
- Hand-drawn art generated externally, processed with Pillow (transparent bg removal)
- Images stored at 2x resolution for Retina, displayed via fixed pixel sizes
