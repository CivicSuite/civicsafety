from fastapi.testclient import TestClient

from civicsafety import __version__
from civicsafety.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicSafety"
    assert payload["version"] == __version__
    assert "CJI ingestion" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civicsafety",
        "version": "0.1.1",
        "civiccore_version": "0.3.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civicsafety").text
    assert "CivicSafety v0.1.1" in text
    assert "No CJI ingestion" in text
    assert "civiccore==0.3.0" in text


def test_api_endpoints_return_deterministic_payloads():
    policy = client.post(
        "/api/v1/civicsafety/policy-answer",
        json={"question": "release policy", "includes_cji": True},
    ).json()
    assert policy["cji_blocked"] is True
    assert policy["supervisor_review_required"] is True

    training = client.post(
        "/api/v1/civicsafety/training-checklist",
        json={"staff_id": "staff-1", "topics": ["SOP"]},
    ).json()
    assert training["excludes_cji"] is True

    pio = client.post(
        "/api/v1/civicsafety/pio-draft",
        json={"topic": "road closure", "facts": ["main street closed"]},
    ).json()
    assert pio["public_information_officer_review_required"] is True

    stats = client.post(
        "/api/v1/civicsafety/public-stats",
        json={"statistics": [{"label": "calls", "count": 5}]},
    ).json()
    assert stats["aggregate_only"] is True
