from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicsafety.pio import draft_public_information_update
from civicsafety.training import build_training_checklist


metadata = sa.MetaData()

training_records = sa.Table(
    "training_records",
    metadata,
    sa.Column("checklist_id", sa.String(36), primary_key=True),
    sa.Column("staff_id", sa.String(255), nullable=False),
    sa.Column("topics", sa.JSON(), nullable=False),
    sa.Column("supervisor_review_required", sa.Boolean(), nullable=False),
    sa.Column("excludes_cji", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicsafety",
)

pio_records = sa.Table(
    "pio_records",
    metadata,
    sa.Column("draft_id", sa.String(36), primary_key=True),
    sa.Column("topic", sa.String(255), nullable=False),
    sa.Column("draft", sa.Text(), nullable=False),
    sa.Column("citations", sa.JSON(), nullable=False),
    sa.Column("public_information_officer_review_required", sa.Boolean(), nullable=False),
    sa.Column("boundary", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicsafety",
)


@dataclass(frozen=True)
class StoredTrainingChecklist:
    checklist_id: str
    staff_id: str
    topics: list[str]
    supervisor_review_required: bool
    excludes_cji: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredPioDraft:
    draft_id: str
    topic: str
    draft: str
    citations: list[str]
    public_information_officer_review_required: bool
    boundary: str
    created_at: datetime


class SafetyWorkpaperRepository:
    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicsafety": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicsafety"))
        metadata.create_all(self.engine)

    def create_training(self, *, staff_id: str, topics: list[str]) -> StoredTrainingChecklist:
        checklist = build_training_checklist(staff_id, topics)
        stored = StoredTrainingChecklist(
            checklist_id=str(uuid4()),
            staff_id=checklist.staff_id,
            topics=list(checklist.topics),
            supervisor_review_required=checklist.supervisor_review_required,
            excludes_cji=checklist.excludes_cji,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(training_records.insert().values(**stored.__dict__))
        return stored

    def get_training(self, checklist_id: str) -> StoredTrainingChecklist | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(training_records).where(training_records.c.checklist_id == checklist_id)
            ).mappings().first()
        return None if row is None else StoredTrainingChecklist(**dict(row))

    def create_pio(self, *, topic: str, facts: list[str]) -> StoredPioDraft:
        draft = draft_public_information_update(topic, facts)
        stored = StoredPioDraft(
            draft_id=str(uuid4()),
            topic=draft.topic,
            draft=draft.draft,
            citations=list(draft.citations),
            public_information_officer_review_required=(
                draft.public_information_officer_review_required
            ),
            boundary=draft.boundary,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(pio_records.insert().values(**stored.__dict__))
        return stored

    def get_pio(self, draft_id: str) -> StoredPioDraft | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(pio_records).where(pio_records.c.draft_id == draft_id)
            ).mappings().first()
        return None if row is None else StoredPioDraft(**dict(row))
