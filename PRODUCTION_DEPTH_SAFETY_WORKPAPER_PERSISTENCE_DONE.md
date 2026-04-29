# CivicSafety Production-Depth Workpaper Persistence

## Summary

CivicSafety now supports optional SQLAlchemy-backed persistence for non-CJI training checklists and PIO drafts. The feature is controlled by `CIVICSAFETY_WORKPAPER_DB_URL`; when it is absent, existing POST endpoints remain stateless and retrieval endpoints return actionable setup guidance.

## Shipped

- `SafetyWorkpaperRepository` with SQLite/local and schema-aware database support.
- Persisted training checklist records with `checklist_id` retrieval.
- Persisted PIO draft records with `draft_id` retrieval.
- API round-trip tests, repository reload tests, and no-config/missing-record error tests.
- Current-facing README, manual, changelog, and landing-page updates.

## Verification

- `python -m pytest --collect-only -q`
- `python -m pytest -q`
- `bash scripts/verify-release.sh`
- Browser QA desktop/mobile for `/docs/index.html`.

## Boundary

CivicSafety persistence is limited to non-CJI administrative workpapers. It still does not ingest CJI, integrate with CAD/RMS, support dispatch, drive enforcement, investigate cases, manage evidence, provide legal advice, call live LLMs, or ship connector runtime.
