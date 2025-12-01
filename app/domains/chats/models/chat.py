from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
