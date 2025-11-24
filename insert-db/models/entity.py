from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class Entity(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    project_id: Optional[uuid.UUID] = Field(default=None, foreign_key="project.id")
    type: str
    raw_data: str
    created_at: Optional[str] = None
