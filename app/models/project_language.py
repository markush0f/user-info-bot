from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class ProjectLanguage(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key="project.id")
    language: str
    bytes: Optional[int] = None
    created_at: Optional[str] = None
