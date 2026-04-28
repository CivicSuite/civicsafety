"""Aggregated public-safety statistics helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicSafetyStatistic:
    label: str
    count: int
    aggregate_only: bool = True


@dataclass(frozen=True)
class PublicStatsSummary:
    statistics: tuple[PublicSafetyStatistic, ...]
    aggregate_only: bool
    cji_excluded: bool
    boundary: str


def summarize_public_statistics(statistics: list[PublicSafetyStatistic]) -> PublicStatsSummary:
    return PublicStatsSummary(
        statistics=tuple(statistics),
        aggregate_only=True,
        cji_excluded=True,
        boundary=(
            "CivicSafety v0.1.1 handles aggregate, public-facing statistics only. It does not "
            "expose incident narratives, evidence, CAD/RMS records, or personally identifying CJI."
        ),
    )
