# Changelog

## [0.1.1] - 2026-04-28

### Changed

- Dependency-alignment release: moved CivicSafety to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.
- Added optional SQLAlchemy-backed non-CJI training checklist and PIO draft workpaper persistence behind `CIVICSAFETY_WORKPAPER_DB_URL`, with retrieval endpoints and actionable setup errors.

## [0.1.0] - 2026-04-27

### Added

- CivicSafety runtime foundation with FastAPI health, root, public UI, and deterministic API endpoints.
- Non-CJIS policy/SOP Q&A, training checklist, PIO draft, and aggregate public-statistics helpers.
- Professional docs, browser QA artifacts, GitHub community templates, placeholder-import gate, release gate, and package build.
