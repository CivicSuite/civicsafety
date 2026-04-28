CivicSafety

CivicSafety v0.1.0 ships municipal public-safety administrative support foundations: cited non-CJIS policy/SOP Q&A, training checklists, PIO draft support, aggregate public-statistics summaries, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not a CAD/RMS integration, dispatch tool, enforcement workflow, investigative workflow, evidence system, CJI ingestion path, legal advice engine, live LLM runtime, or public-safety connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civicsafety.main:app --host 127.0.0.1 --port 8143

CivicSafety v0.1.0 is pinned to civiccore==0.2.0.

Apache 2.0 code. CC BY 4.0 docs.
