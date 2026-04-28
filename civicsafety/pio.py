"""Public-information draft helpers for non-CJIS public-safety communications."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PioDraft:
    topic: str
    draft: str
    citations: tuple[str, ...]
    public_information_officer_review_required: bool
    boundary: str


def draft_public_information_update(topic: str, facts: list[str]) -> PioDraft:
    return PioDraft(
        topic=topic,
        draft=f"Draft public-safety information update about {topic}: " + "; ".join(facts),
        citations=("Public Information Office review checklist",),
        public_information_officer_review_required=True,
        boundary=(
            "Draft only: CivicSafety does not publish, advocate, investigate, disclose CJI, "
            "or replace official PIO approval."
        ),
    )
