from sqlmodel import SQLModel, Field, Column, DateTime
from uuid import uuid4, UUID
from datetime import datetime


class Message(SQLModel, table=True):
    __tablename__ = "messages"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    chat_id: UUID = Field(foreign_key="chats.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
