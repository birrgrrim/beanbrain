# CLAUDE.md — BeanBrain

## Project Overview
BeanBrain is a personal coffee tracking tool for managing coffee beans, grinder settings, and reviews. Built for local use.

## Stack
- **Backend**: Python 3.12+ / FastAPI / SQLAlchemy / SQLite
- **Frontend**: SvelteKit (adapter-node) / Tailwind CSS v4 / TypeScript
- **Package manager**: uv (Python), npm (Node)
- **Deploy**: launchd + Caddy reverse proxy, `services` user
- **No Docker** — runs locally with `make dev`

## Running
```bash
make setup-backend    # uv sync
make setup-frontend   # npm install
make dev              # starts both (backend :8001, frontend :5173)
make test             # runs backend pytest
```

Dev ports: backend :8001, frontend :5173 (prod uses :8000/:3000 to avoid conflicts).

## Project Structure
```
backend/
  app/
    main.py           # FastAPI app with lifespan, CORS (env-configurable)
    models.py         # SQLAlchemy models (Coffee, Review, Equipment, etc.)
    schemas.py        # Pydantic request/response schemas
    database.py       # SQLite engine + session (DATABASE_URL env)
    seed.py           # Initial data (descriptors, origins)
    routers/          # API endpoints (coffees, reviews, equipment, scrape, etc.)
    scrapers/         # Roastery scrapers (MadHeads implemented)
  tests/              # pytest with in-memory SQLite
frontend/
  src/
    app.css           # Tailwind + custom theme (parchment colors)
    lib/
      api.ts          # Typed API client (relative /api in prod, localhost in dev)
      i18n.ts         # EN/UA translations (~130 keys)
      lang.ts         # Language store (localStorage, SSR-safe)
      personStore.ts  # Active person store (localStorage, SSR-safe)
      refData.ts      # Cached reference data (origins, descriptors, etc.)
      utils.ts        # Shared utilities (toggleId)
      components/     # Svelte components (21 components)
    routes/
      +page.svelte    # Main SPA (responsive sidebar + panel, tab switching)
      +layout.svelte  # Root layout (fonts, favicon, base styles)
  static/img/         # Hand-drawn illustrations (transparent PNGs)
```

## Key Design Decisions
- **One review per person per coffee** — upsert via PUT, not multiple tastings
- **Coffee stock tracking** — `in_stock` (at home) + `in_store` (at roastery), independent booleans
- **Equipment defaults** — `is_default` on grinder/method, used for sidebar display
- **MadHeads scraper** — parses SvelteKit embedded data from HTML, supports EN/UK, all 18 products validated
- **Bean rating** — hand-drawn coffee bean images (full/half/empty) replace star SVGs
- **Responsive font** — 16px mobile, 18px desktop
- **SSR-safe localStorage** — guarded with `typeof window !== 'undefined'` (Node 22+ has broken localStorage global)

## Design Language
- **Color**: Warm parchment palette (`#f4ecdd` bg, `#faf6ee` cards, amber accents)
- **Typography**: DM Serif Display (headings) + DM Sans (body)
- **Art**: Hand-drawn coffee illustrations, transparent PNGs, consistent sepia/brown style
- **Logo**: Bean-brain icon (coffee bean + circuit board), with text variant
- **Layout**: Responsive — sidebar (full/320/420px) + content panel, tab navigation (Coffee/Grind/Brew/Roast)
  - xl (1280px+): 2-column with tab labels, logo with text
  - md-xl: sidebar + detail, icon-only tabs
  - mobile (<768px): single panel mode (sidebar OR detail)

## API Patterns
- Coffees: `GET/POST /coffees/`, `GET/PUT/DELETE /coffees/{id}`, `POST /coffees/{id}/refresh`
- Reviews: `PUT /coffees/{id}/reviews/` (upsert), `DELETE /coffees/{id}/reviews/{rid}`
- Grinder settings: `POST/DELETE /coffees/{id}/settings/`
- Equipment CRUD: `GET/POST/PUT/DELETE /grinders`, `/brew-setups`
- Roasteries: `GET/POST/PUT/DELETE /roasteries/`, `POST /roasteries/{id}/refresh`
- Scrape: `GET /scrape/?url=...`
- Coffee list returns `avg_rating`, `person_rating`, `default_grind` computed fields

## Testing
- Backend: pytest with in-memory SQLite (70 tests), ruff linting
- Frontend: svelte-check type validation + production build verification
- Run: `cd backend && uv run pytest tests/ -v`
- Lint: `cd backend && uv run ruff check .`
- CI: GitHub Actions runs on every push to `main` and on PRs

## Git Workflow
- **`main` branch**: direct pushes only for critical/short fixes (typos, broken prod, etc.)
- **All other work**: create an issue → branch → PR → merge after CI passes
- **Branches**: use descriptive prefixes (`ci/`, `feat/`, `fix/`, `design/`, etc.)
- **Milestones**: group related issues into milestones for releases
- **Releases**: semantic versioning, CHANGELOG.md updated with each release
- **Version**: update `frontend/package.json` and `backend/pyproject.toml` version on release
- **PR merge**: user hand-tests the deployed result before merging — never auto-merge

### Milestone strategies
- **Independent fixes** (e.g. v0.2.0 — polish/bugs): each issue gets its own branch → PR to `main`
- **Coupled changes** (e.g. v0.3.0 — migrations + schema): create a `milestone/vX.Y.Z` branch, feature branches PR into it, final PR to `main` after integration testing

## Conventions
- Commits co-authored with Claude
- Ukrainian translations maintained alongside English
- Hand-drawn art generated externally, processed with Pillow (transparent bg removal)
- Images stored at 2x resolution for Retina, displayed via fixed pixel sizes
- `uv.lock` committed for reproducible deploys
