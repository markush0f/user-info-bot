from uuid import UUID, uuid4
from app.domains.messages.models.message import Message
from core.db import get_session
from infrastructure.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self):
        pass

    def create_message(self, message: Message) -> Message:
        # Added message creation using repository
        with get_session() as session:
            repo = MessageRepository(session)
            msg = Message(id=uuid4(), chat_id=message.chat_id, role=message.role, content=message.content)
            return repo.create(msg)

    def get_messages_by_chat(self, chat_id: UUID) -> list[Message]:
        # Added retrieval of all chat messages
        with get_session() as session:
            repo = MessageRepository(session)
            return repo.get_all_by_chat(chat_id)

    def get_last_messages(self, chat_id: UUID, limit: int = 10) -> list[Message]:
        # Added retrieval of the latest N messages
        with get_session() as session:
            repo = MessageRepository(session)
            return repo.get_last_n(chat_id, limit)

    def delete_messages_by_chat(self, chat_id: UUID):
        # Added deletion of all messages of a chat
        with get_session() as session:
            repo = MessageRepository(session)
            repo.delete_by_chat(chat_id)
