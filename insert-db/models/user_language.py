from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class UserLanguage(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    language: str
    bytes: Optional[int] = None
    repos_count: Optional[int] = None
    created_at: Optional[str] = None
