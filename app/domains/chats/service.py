from uuid import UUID, uuid4
from app.domains.chats.models.chat import Chat
from app.domains.messages.models.message import Message
from core.db import get_session

from infrastructure.repositories.chat_repository import ChatRepository
from infrastructure.repositories.message_repository import MessageRepository
from domains.embeddings.vector_search_service import VectorSearchService
from domains.documents.rag_context_builder import RagContextBuilder
from infrastructure.llm.llm_client import LLMClient


class ChatService:
    def __init__(self):
        self.session = get_session()
        self.chat_repo = ChatRepository(self.session)
        self.message_repo = MessageRepository(self.session)
        self.vector_service = VectorSearchService()
        self.context_builder = RagContextBuilder()
        self.llm = LLMClient()

    async def send_message(self, chat_id: UUID, user_id: UUID, message: str) -> str:
        chat = self.chat_repo.get_by_id(chat_id)
        if not chat:
            chat = Chat(id=uuid4(), user_id=user_id)
            self.chat_repo.create(chat)

        user_msg = Message(id=uuid4(), chat_id=chat.id, role="user", content=message)
        self.message_repo.create(user_msg)

        history = self.message_repo.get_last_n(chat.id, limit=10)

        retrieved_chunks = await self.vector_service.search(message, str(user_id))

        rag_context = self.context_builder.build(message, retrieved_chunks)

        history_text = "\n".join(f"{m.role.upper()}: {m.content}" for m in history)

        prompt = f"""
        You are a contextual assistant. Use both conversation history and retrieved context.
        If an answer is not in the context, say that you do not know.

        Conversation history:
        {history_text}

        Retrieved context:
        {rag_context}

        User message:
        {message}
        """

        # Added LLM generation using injected client
        assistant_reply = self.llm.generate(prompt)

        # Added assistant message persistence
        assistant_msg = Message(
            id=uuid4(), chat_id=chat.id, role="assistant", content=assistant_reply
        )
        self.message_repo.create(assistant_msg)

        return assistant_reply
