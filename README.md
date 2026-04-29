# CivicSafety

CivicSafety v0.1.1 ships the municipal public-safety administrative support foundation for CivicSuite: cited non-CJIS policy/SOP Q&A, training checklists, PIO draft support, aggregate public-statistics summaries, optional database-backed training/PIO workpapers, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not a CAD/RMS integration, dispatch tool, enforcement workflow, investigative workflow, evidence system, CJI ingestion path, legal advice engine, live LLM runtime, or public-safety connector.

Install:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicsafety.main:app --host 127.0.0.1 --port 8143
```

CivicSafety v0.1.1 is pinned to `civiccore==0.3.0`.

Optional workpaper persistence is available with `CIVICSAFETY_WORKPAPER_DB_URL`. Set it to a SQLAlchemy database URL to store generated non-CJI training checklists and PIO drafts for later supervisor/PIO review. If unset, POST endpoints remain stateless and retrieval endpoints return an actionable setup message.

Apache 2.0 code. CC BY 4.0 docs.
