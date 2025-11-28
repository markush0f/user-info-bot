from sqlmodel import SQLModel, Field, Column
from typing import Optional, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import JSONB


class Entity(SQLModel, table=True):
    __tablename__ = "entities"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    project_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="projects.id",
        nullable=True,
    )
    type: str
    raw_data: Dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
    created_at: Optional[str] = None
    summary: str
