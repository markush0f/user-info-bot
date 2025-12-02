from uuid import UUID, uuid4
from app.domains.messages.models.message import Message
from app.infrastructure.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, session):
        # Added: inject session instead of creating a new one
        self.session = session
        self.repository = MessageRepository(session)

    def create_message(self, message: Message) -> Message:
        # Added: message creation using injected session and repository
        msg = Message(
            id=uuid4(),
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
        )
        message = self.repository.create(msg)
        self.session.commit()
        return message

    def get_messages_by_chat(self, chat_id: UUID) -> list[Message]:
        return self.repository.get_all_by_chat(chat_id)

    def get_last_messages(self, chat_id: UUID, limit: int = 10) -> list[Message]:
        return self.repository.get_last_n(chat_id, limit)

    def delete_messages_by_chat(self, chat_id: UUID):
        self.repository.delete_by_chat(chat_id)
        self.session.commit()

