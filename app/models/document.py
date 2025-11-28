from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Document(SQLModel, table=True):
    __tablename__ = "documents" # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    entity_id: uuid.UUID = Field(nullable=False, foreign_key="entities.id")
    title: str | None = Field(default=None)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
