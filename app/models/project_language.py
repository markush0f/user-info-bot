import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime


class ProjectLanguage(SQLModel, table=True):
    __tablename__ = "project_languages" # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(nullable=False, foreign_key="projects.id")
    language: str = Field(nullable=False)
    bytes: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)