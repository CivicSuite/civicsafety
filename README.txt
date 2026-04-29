CivicSafety

CivicSafety v0.1.1 ships municipal public-safety administrative support foundations: cited non-CJIS policy/SOP Q&A, training checklists, PIO draft support, aggregate public-statistics summaries, optional database-backed training/PIO workpapers, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

Optional workpaper persistence: set CIVICSAFETY_WORKPAPER_DB_URL to a SQLAlchemy database URL to store generated non-CJI training checklists and PIO drafts. Without it, POST endpoints stay stateless and retrieval endpoints explain how to enable storage.

It is not a CAD/RMS integration, dispatch tool, enforcement workflow, investigative workflow, evidence system, CJI ingestion path, legal advice engine, live LLM runtime, or public-safety connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civicsafety.main:app --host 127.0.0.1 --port 8143

CivicSafety v0.1.1 is pinned to civiccore==0.3.0.

Apache 2.0 code. CC BY 4.0 docs.
