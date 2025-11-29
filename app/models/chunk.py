from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime


class Chunk(SQLModel, table=True):
    __tablename__ = "chunks"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(nullable=False, foreign_key="documents.id")
    chunk_index: int = Field(nullable=False)
    chunk_text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
