# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-03-21

### Added
- Alembic database migration mechanism with autogenerate and SQLite batch mode
- Migrations auto-applied on backend startup
- Baseline migration stamping existing databases
- Centralized backup script with version + migration number in filenames (`beanbrain-0.3.0-m001-2026-03-21.db`)

### Changed
- Replaced hand-rolled `schema_version` table with Alembic's `alembic_version`
- Release tarball now includes `migrations/` and `deploy/` directories
- Versioning strategy: schema-changing issues get individual minor version bumps
- Backend test count: 92 → 91 (removed SchemaVersion test, replaced by Alembic)

## [0.2.0] - 2026-03-21

### Fixed
- Resize and compress art assets — 16 MB → 1.2 MB (92% reduction) for instant mobile loads
- Replace `transition: all` global CSS rule to prevent layout shifts on resize

### Added
- Test coverage for scrape/refresh endpoints (14 new tests with mocked HTTP)
- Version-stamped backups (`beanbrain-0.2.0-2026-03-21.db`) and `schema_version` DB table
- Loading skeleton placeholders with parchment shimmer animation in CoffeeDetail
- Retry with exponential backoff (1s, 3s, 9s) on transient scrape errors
- User-friendly scrape error messages ("Roastery site timed out", "Product page not found")
- Inline error display for coffee and roastery refresh failures
- Unit tests for retry logic (7 tests)

### Changed
- Frontend API client reads `detail` field from error responses
- Removed 6 unused SVG icons from Icons.svelte (replaced by PNG art)
- Backend test count: 70 → 92

## [0.1.0] - 2026-03-20

### Added
- Coffee catalog with roastery, origin, process, roast level, score, taste profile, prices
- Auto-fill from MadHeads roastery URLs (scraper with EN/UK support)
- Refresh & batch refresh for scraped coffees
- Grinder settings per coffee/grinder/brew setup combination
- Reviews with one-review-per-person upsert, bean icon rating, taste descriptors
- Roastery vs personal taste descriptor comparison
- Stock tracking (at home / in store) with stock-priority sorting
- Equipment management (grinders, brew setups, brew method types)
- Bilingual interface (EN/UA) with one-click toggle
- Responsive layout (desktop 2-column, tablet compact, mobile single-panel)
- Hand-drawn coffee illustrations and parchment theme
- GitHub Actions CI (backend tests + lint, frontend type check + build)
- Backend test suite (70 tests covering all CRUD endpoints)
- Ruff linter for backend code
- Version label in header bar

[0.3.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.0
[0.2.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.2.0
[0.1.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.1.0
