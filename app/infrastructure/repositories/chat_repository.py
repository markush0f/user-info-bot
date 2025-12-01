from sqlmodel import Session, select
from domains.chat.models.chat import Chat
from uuid import UUID


class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, chat: Chat) -> Chat:
        self.session.add(chat)
        self.session.commit()
        self.session.refresh(chat)
        return chat

    def get_by_id(self, chat_id: UUID) -> Chat | None:
        return self.session.get(Chat, chat_id)

    def get_all_by_user(self, user_id: UUID) -> list[Chat]:
        statement = select(Chat).where(Chat.user_id == user_id)
        return list(self.session.exec(statement))

    def delete(self, chat_id: UUID):
        chat = self.get_by_id(chat_id)
        if chat:
            self.session.delete(chat)
            self.session.commit()
