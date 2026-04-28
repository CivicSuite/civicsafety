from civicsafety import __version__
from civicsafety.pio import draft_public_information_update
from civicsafety.policy import SafetyPolicySource, answer_policy_question
from civicsafety.stats import PublicSafetyStatistic, summarize_public_statistics
from civicsafety.training import build_training_checklist


def test_version_is_release_version():
    assert __version__ == "0.1.1"


def test_policy_answer_blocks_cji_and_requires_review():
    answer = answer_policy_question(
        "Can we summarize this SOP?",
        [
            SafetyPolicySource("public", "SOP", "Use public policy text.", "SOP-1"),
            SafetyPolicySource("cji", "Incident detail", "restricted", "CJI", contains_cji=True),
        ],
    )
    assert answer.citations == ("SOP-1",)
    assert answer.supervisor_review_required is True
    assert answer.cji_blocked is True
    assert "does not ingest CJI" in answer.boundary


def test_training_checklist_is_non_cji():
    checklist = build_training_checklist("staff-1", ["policy review", "PIO protocol"])
    assert checklist.supervisor_review_required is True
    assert checklist.excludes_cji is True
    assert checklist.topics == ("policy review", "PIO protocol")


def test_pio_draft_requires_review_and_does_not_publish():
    draft = draft_public_information_update("storm readiness", ["shelter opens at 6 PM"])
    assert draft.public_information_officer_review_required is True
    assert "does not publish" in draft.boundary
    assert draft.citations == ("Public Information Office review checklist",)


def test_public_stats_are_aggregate_only():
    summary = summarize_public_statistics([PublicSafetyStatistic("calls for service", 42)])
    assert summary.aggregate_only is True
    assert summary.cji_excluded is True
    assert "does not expose incident narratives" in summary.boundary
