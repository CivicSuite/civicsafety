"""Non-CJI training checklist helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingChecklist:
    staff_id: str
    topics: tuple[str, ...]
    supervisor_review_required: bool
    excludes_cji: bool


def build_training_checklist(staff_id: str, topics: list[str]) -> TrainingChecklist:
    return TrainingChecklist(
        staff_id=staff_id,
        topics=tuple(topics),
        supervisor_review_required=True,
        excludes_cji=True,
    )
