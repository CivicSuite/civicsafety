"""FastAPI runtime foundation for CivicSafety."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicsafety import __version__
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
            "aggregate public statistics, and public UI foundation are online; CJI ingestion, "
            "CAD/RMS integration, dispatch, enforcement, investigations, evidence workflows, "
            "legal advice, live LLM calls, and connector runtime are not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: isolated deployment profile and CJIS-gated adapter design",
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
    return build_training_checklist(request.staff_id, request.topics).__dict__


@app.post("/api/v1/civicsafety/pio-draft")
def pio_draft(request: PioDraftRequest) -> dict[str, object]:
    return draft_public_information_update(request.topic, request.facts).__dict__


@app.post("/api/v1/civicsafety/public-stats")
def public_stats(request: PublicStatsRequest) -> dict[str, object]:
    return summarize_public_statistics(request.statistics).__dict__
