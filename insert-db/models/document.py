from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class Document(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    entity_id: uuid.UUID = Field(default=None, foreign_key="entity.id")
    title: Optional[str] = None
    content: str
    created_at: Optional[str] = None
