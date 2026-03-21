# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.4] - 2026-03-22

### Added
- Context switcher — person, grinder, brew method as compact header selectors with popovers
- EditDialog modal for adding/editing all equipment types with full fields
- Delete with cascade confirmation showing dependent record counts
- Avatar system — preset icons + custom image upload for persons, grinders, brew setups
- 4 hand-drawn person avatar presets (transparent backgrounds)
- Avatar upload endpoint with Pillow resize to 128x128
- `PUT /tasters/{id}` endpoint for rename
- Dependents count endpoints for cascade confirmation

### Changed
- Removed Grind and Brew sidebar tabs (replaced by header context switcher)
- Removed `is_default` from grinders and brew setups — all context selection is frontend-only (localStorage)
- Removed "Everyone" mode — person must always be selected
- Removed seed equipment (no more "Default Grinder")
- Grind settings and reviews use active context (person/grinder/brew) instead of inline selectors
- Shows "Edit" when entry exists for current context, "+ Add" when not
- Delete inside edit form only — removed per-item buttons from lists
- Right-aligned grind values and review ratings
- Review rating as number only in list (no stars, no /10)
- Consistent vertical layout for equipment info in grind/review lists
- Backend test count: 92 → 88 (removed is_default toggle tests)

### Removed
- GrindingSidebar and BrewingSidebar tabs
- `is_default` column from grinders and brew_setups tables
- PersonSwitcher component (replaced by ContextSwitcher)

## [0.3.3] - 2026-03-21

### Added
- Per-brew-method reviews — same person can rate same coffee differently per brew method
- Brew method selector in review form
- Brew method badge on each review display
- New test: `test_per_method_reviews` (92 tests total)

### Changed
- Review unique constraint: `(coffee_id, taster_id)` → `(coffee_id, taster_id, brew_setup_id)`
- Sidebar person rating filters by default brew setup
- Migration backfills existing reviews with default brew setup

## [0.3.2] - 2026-03-21

### Changed
- Grinder: `name` field renamed to `manufacturer`
- Brew setup: `name` field replaced with `manufacturer` + `model` (consistent with grinders)
- Unified equipment display: one-line name in sidebars, full name at back button, separate lines in detail cards
- Grinder sidebar shows range and step info on second line
- Updated form placeholders (e.g. "Eureka" + "Mignon Specialita")

## [0.3.1] - 2026-03-21

### Added
- Grinder config: `range_min`, `range_max`, `step` fields with Alembic migration
- GrindValue component: integer part normal size, decimal part (`.5`) in smaller font
- Range and step fields in grinder create/edit forms
- Grinder setting input respects grinder's min/max/step constraints
- Coffee list refreshes when default grinder or brew setup changes

### Fixed
- Sidebar spacing: wider number area and gap between icons and values
- Orphaned grinder setting crash (brew setup FK without cascade)

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

[0.3.4]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.4
[0.3.3]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.3
[0.3.2]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.2
[0.3.1]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.1
[0.3.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.3.0
[0.2.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.2.0
[0.1.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.1.0
