"""FastAPI runtime foundation for CivicSafety."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicsafety import __version__
from civicsafety.persistence import SafetyWorkpaperRepository, StoredPioDraft, StoredTrainingChecklist
from civicsafety.pio import draft_public_information_update
from civicsafety.policy import SafetyPolicySource, answer_policy_question
from civicsafety.public_ui import render_public_lookup_page
from civicsafety.stats import PublicSafetyStatistic, summarize_public_statistics
from civicsafety.training import build_training_checklist

app = FastAPI(
    title="CivicSafety",
    version=__version__,
    description="Non-CJIS public-safety administrative support foundation for CivicSuite.",
)

_workpaper_repository: SafetyWorkpaperRepository | None = None
_workpaper_db_url: str | None = None

@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)

POLICY_SOURCES = [
    SafetyPolicySource(
        "sop-1",
        "General Order 100",
        "PIO releases, SOP summaries, and training reminders must avoid CJI.",
        "General Order 100",
    )
]


class PolicyQuestionRequest(BaseModel):
    question: str
    includes_cji: bool = False


class TrainingChecklistRequest(BaseModel):
    staff_id: str
    topics: list[str]


class PioDraftRequest(BaseModel):
    topic: str
    facts: list[str]


class PublicStatsRequest(BaseModel):
    statistics: list[PublicSafetyStatistic]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicSafety",
        "version": __version__,
        "status": "non-CJIS public-safety admin foundation",
        "message": (
            "CivicSafety policy/SOP Q&A, non-CJI training checklists, PIO draft support, "
            "aggregate public statistics, optional database-backed training/PIO workpapers, "
            "and public UI foundation are online; CJI ingestion, "
            "CAD/RMS integration, dispatch, enforcement, investigations, evidence workflows, "
            "legal advice, live LLM calls, and connector runtime are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: isolated deployment profile and CJIS-gated adapter design",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civicsafety",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicsafety", response_class=HTMLResponse)
def public_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civicsafety/policy-answer")
def policy_answer(request: PolicyQuestionRequest) -> dict[str, object]:
    sources = list(POLICY_SOURCES)
    if request.includes_cji:
        sources.append(
            SafetyPolicySource("blocked", "CJI-marked material", "restricted", "CJI", True)
        )
    return answer_policy_question(request.question, sources).__dict__


@app.post("/api/v1/civicsafety/training-checklist")
def training_checklist(request: TrainingChecklistRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        return _stored_training_response(
            _get_workpaper_repository().create_training(
                staff_id=request.staff_id,
                topics=request.topics,
            )
        )
    payload = build_training_checklist(request.staff_id, request.topics).__dict__
    payload["checklist_id"] = None
    return payload


@app.get("/api/v1/civicsafety/training-checklist/{checklist_id}")
def get_training_checklist(checklist_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicSafety workpaper persistence is not configured.",
                "fix": "Set CIVICSAFETY_WORKPAPER_DB_URL to retrieve persisted training checklists.",
            },
        )
    stored = _get_workpaper_repository().get_training(checklist_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Training checklist record not found.",
                "fix": "Use a checklist_id returned by POST /api/v1/civicsafety/training-checklist.",
            },
        )
    return _stored_training_response(stored)


@app.post("/api/v1/civicsafety/pio-draft")
def pio_draft(request: PioDraftRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        return _stored_pio_response(
            _get_workpaper_repository().create_pio(topic=request.topic, facts=request.facts)
        )
    payload = draft_public_information_update(request.topic, request.facts).__dict__
    payload["draft_id"] = None
    return payload


@app.get("/api/v1/civicsafety/pio-draft/{draft_id}")
def get_pio_draft(draft_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicSafety workpaper persistence is not configured.",
                "fix": "Set CIVICSAFETY_WORKPAPER_DB_URL to retrieve persisted PIO drafts.",
            },
        )
    stored = _get_workpaper_repository().get_pio(draft_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "PIO draft record not found.",
                "fix": "Use a draft_id returned by POST /api/v1/civicsafety/pio-draft.",
            },
        )
    return _stored_pio_response(stored)


@app.post("/api/v1/civicsafety/public-stats")
def public_stats(request: PublicStatsRequest) -> dict[str, object]:
    return summarize_public_statistics(request.statistics).__dict__


def _workpaper_database_url() -> str | None:
    return os.environ.get("CIVICSAFETY_WORKPAPER_DB_URL")


def _get_workpaper_repository() -> SafetyWorkpaperRepository:
    global _workpaper_db_url, _workpaper_repository
    db_url = _workpaper_database_url()
    if db_url is None:
        raise RuntimeError("CIVICSAFETY_WORKPAPER_DB_URL is not configured.")
    if _workpaper_repository is None or db_url != _workpaper_db_url:
        _dispose_workpaper_repository()
        _workpaper_db_url = db_url
        _workpaper_repository = SafetyWorkpaperRepository(db_url=db_url)
    return _workpaper_repository


def _dispose_workpaper_repository() -> None:
    global _workpaper_repository
    if _workpaper_repository is not None:
        _workpaper_repository.engine.dispose()
        _workpaper_repository = None


def _stored_training_response(stored: StoredTrainingChecklist) -> dict[str, object]:
    return {**stored.__dict__, "created_at": stored.created_at.isoformat()}


def _stored_pio_response(stored: StoredPioDraft) -> dict[str, object]:
    return {**stored.__dict__, "created_at": stored.created_at.isoformat()}
