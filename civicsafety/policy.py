"""Non-CJIS policy and SOP Q&A helpers for CivicSafety."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyPolicySource:
    source_id: str
    title: str
    text: str
    citation: str
    contains_cji: bool = False


@dataclass(frozen=True)
class SafetyPolicyAnswer:
    answer: str
    citations: tuple[str, ...]
    supervisor_review_required: bool
    cji_blocked: bool
    boundary: str


def answer_policy_question(
    question: str, sources: list[SafetyPolicySource]
) -> SafetyPolicyAnswer:
    usable_sources = [source for source in sources if not source.contains_cji]
    blocked = len(usable_sources) != len(sources)
    citations = tuple(source.citation for source in usable_sources if source.text)
    return SafetyPolicyAnswer(
        answer=(
            f"Draft non-CJIS public-safety policy answer for: {question}. "
            "Verify against the cited SOP or general order before use."
        ),
        citations=citations,
        supervisor_review_required=True,
        cji_blocked=blocked,
        boundary=(
            "CivicSafety supports non-CJIS administrative policy work only. It does not ingest "
            "CJI, connect to CAD/RMS, support dispatch, investigate cases, or drive enforcement."
        ),
    )
