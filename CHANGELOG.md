# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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

[0.1.0]: https://github.com/birrgrrim/beanbrain/releases/tag/v0.1.0
