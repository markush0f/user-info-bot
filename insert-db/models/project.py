from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
    repo_name: str
    description: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    last_commit: Optional[str] = None
    created_at: Optional[str] = None
