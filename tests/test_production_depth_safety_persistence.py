from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civicsafety.main import app, _dispose_workpaper_repository
from civicsafety.persistence import SafetyWorkpaperRepository


client = TestClient(app)


def test_repository_persists_training_and_pio(tmp_path: Path) -> None:
    db_path = tmp_path / "civicsafety.db"
    repo = SafetyWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    checklist = repo.create_training(staff_id="staff-1", topics=["PIO protocol"])
    draft = repo.create_pio(topic="road closure", facts=["main street closed"])
    repo.engine.dispose()

    reloaded = SafetyWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    assert reloaded.get_training(checklist.checklist_id).excludes_cji is True
    assert reloaded.get_pio(draft.draft_id).topic == "road closure"
    reloaded.engine.dispose()
    db_path.unlink()


def test_safety_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicsafety-api.db"
    monkeypatch.setenv("CIVICSAFETY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    checklist = client.post(
        "/api/v1/civicsafety/training-checklist",
        json={"staff_id": "staff-1", "topics": ["SOP"]},
    )
    fetched_checklist = client.get(
        f"/api/v1/civicsafety/training-checklist/{checklist.json()['checklist_id']}"
    )
    draft = client.post(
        "/api/v1/civicsafety/pio-draft",
        json={"topic": "road closure", "facts": ["main street closed"]},
    )
    fetched_draft = client.get(f"/api/v1/civicsafety/pio-draft/{draft.json()['draft_id']}")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICSAFETY_WORKPAPER_DB_URL")

    assert fetched_checklist.status_code == 200
    assert fetched_checklist.json()["excludes_cji"] is True
    assert fetched_draft.status_code == 200
    assert fetched_draft.json()["public_information_officer_review_required"] is True
    db_path.unlink()


def test_get_training_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICSAFETY_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicsafety/training-checklist/example")
    assert response.status_code == 503
    assert "Set CIVICSAFETY_WORKPAPER_DB_URL" in response.json()["detail"]["fix"]


def test_get_pio_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicsafety-missing.db"
    monkeypatch.setenv("CIVICSAFETY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicsafety/pio-draft/missing")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICSAFETY_WORKPAPER_DB_URL")

    assert response.status_code == 404
    assert "POST /api/v1/civicsafety/pio-draft" in response.json()["detail"]["fix"]
    db_path.unlink()
