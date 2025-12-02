from uuid import UUID, uuid4
from app.shared.services.rag_context_builder import RagContextBuilder
from app.shared.services.record_finder import RecordFinder
from app.domains.chats.models.chat import Chat
from app.domains.messages.models.message import Message
from app.core.db import get_session

from app.infrastructure.repositories.chat_repository import ChatRepository
from app.infrastructure.repositories.message_repository import MessageRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.domains.embeddings.vector_search_service import VectorSearchService
from app.infrastructure.llm.llm_client import LLMClient
from app.domains.users.service import UserService


class ChatService:
    def __init__(self, session):
        self.session = session
        self.chat_repo = ChatRepository(self.session)
        self.message_repo = MessageRepository(self.session)
        self.user_service = UserService(self.session)
        self.vector_service = VectorSearchService(self.session)
        self.context_builder = RagContextBuilder()
        self.llm = LLMClient()

    def create_chat(self, user_id: UUID) -> Chat:
        self.user_service.get_user_or_404(user_id)
        chat = Chat(id=uuid4(), user_id=user_id)
        chat_createad = self.chat_repo.create(chat)
        self.session.commit()
        return chat_createad

    def delete_chat(self, chat_id: UUID):
        RecordFinder(self.chat_repo).find_or_404(chat_id)
        self.chat_repo.delete(chat_id)
        self.session.commit()

    def get_chat(self, chat_id: UUID) -> Chat:
        return RecordFinder(self.chat_repo).find_or_404(chat_id)

    def get_chats_by_user(self, user_id: UUID):
        self.user_service.get_user_or_404(user_id)
        chats = self.chat_repo.get_all_by_user(user_id)
        return [
            {"chat_id": chat.id, "created_at": chat.created_at, "user_id": chat.user_id}
            for chat in chats
        ]

    async def send_message(self, chat_id: UUID, user_id: UUID, content: str) -> str:
        chat = self._ensure_chat(chat_id, user_id)
        self._store_user_message(chat.id, content)

        history = self.message_repo.get_last_n(chat.id, limit=10)
        rag_context = await self._create_rag_context(content, user_id)
        prompt = self._create_prompt(history, rag_context, content)

        assistant_reply = self.llm.generate(prompt)
        self._store_assistant_message(chat.id, assistant_reply)

        return assistant_reply

    def _ensure_chat(self, chat_id: UUID, user_id: UUID) -> Chat:
        self.user_service.get_user_or_404(user_id)
        return self.chat_repo.get_by_id(chat_id) or self.create_chat(user_id)


    def _store_user_message(self, chat_id: UUID, content: str):
        msg = Message(id=uuid4(), chat_id=chat_id, role="user", content=content)
        self.message_repo.create(msg)
        self.session.commit()  


    def _store_assistant_message(self, chat_id: UUID, content: str):
        msg = Message(id=uuid4(), chat_id=chat_id, role="assistant", content=content)
        self.message_repo.create(msg)
        self.session.commit()  

    async def _create_rag_context(self, content: str, user_id: UUID) -> str:
        chunks = await self.vector_service.search(content, str(user_id))
        return self.context_builder.build(content, chunks)

    def _create_prompt(self, history, rag_context: str, user_input: str) -> str:
        history_text = "\n".join(f"{m.role.upper()}: {m.content}" for m in history)

        return f"""
You are a contextual assistant. Use conversation history and retrieved context.
If the answer is not in the context, say you do not know.

Conversation history:
{history_text}

Retrieved context:
{rag_context}

User message:
{user_input}
"""
