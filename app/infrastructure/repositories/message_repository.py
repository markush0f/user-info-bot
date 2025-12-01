from sqlmodel import Session
from sqlalchemy import text
from domains.chat.models.message import Message
from uuid import UUID


class MessageRepository:
    def __init__(self, session: Session):
        # Added DB session dependency
        self.session = session

    def create(self, message: Message) -> Message:
        # Added message persistence
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_by_id(self, message_id: UUID) -> Message | None:
        # Added retrieval by PK
        return self.session.get(Message, message_id)

    def get_all_by_chat(self, chat_id: UUID) -> list[Message]:
        # Added SQL query with manual ordering
        sql = text(
            """
            SELECT * FROM messages
            WHERE chat_id = :chat_id
            ORDER BY created_at ASC
        """
        )

        rows = self.session.execute(sql, {"chat_id": str(chat_id)}).fetchall()
        return [Message(**dict(row)) for row in rows]

    def get_last_n(self, chat_id: UUID, limit: int) -> list[Message]:
        # Added SQL query for last N messages
        sql = text(
            """
            SELECT * FROM messages
            WHERE chat_id = :chat_id
            ORDER BY created_at DESC
            LIMIT :limit
        """
        )

        rows = self.session.execute(
            sql, {"chat_id": str(chat_id), "limit": limit}
        ).fetchall()

        messages = [Message(**dict(row)) for row in rows]
        return messages[::-1]

    def delete_by_chat(self, chat_id: UUID):
        # Added deletion SQL
        sql = text(
            """
            DELETE FROM messages
            WHERE chat_id = :chat_id
        """
        )

        self.session.execute(sql, {"chat_id": str(chat_id)})
        self.session.commit()
