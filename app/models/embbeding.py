from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from typing import Any, List
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector


class Embedding(SQLModel, table=True):
    __tablename__ = "embeddings"   # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  

    chunk_id: uuid.UUID = Field(nullable=False, foreign_key="chunks.id")  

    embedding: List[float] | Any = Field(
        sa_type=Vector(1536),
        nullable=False
    ) 

    created_at: datetime = Field(default_factory=datetime.utcnow)  
