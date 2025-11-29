import uuid
from openai import OpenAI
from app.db import get_session
from app.models.embbeding import Embedding
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import EmbeddingRepository
from app.services.chunk_service import ChunkService


class EmbeddingService:
    def __init__(self):
        self.session = get_session()
        self.document_repository = DocumentRepository(self.session)
        self.chunk_repository = ChunkRepository(self.session)
        self.embedding_repository = EmbeddingRepository(self.session)
        self.chunk_service = ChunkService()
        self.client = OpenAI()

    def _embed(self, text: str):
        response = self.client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding

    def create_embeddings_for_chunks(self, chunk_ids: list[uuid.UUID]):
        created = []

        for chunk_id in chunk_ids:
            chunk = self.chunk_repository.get_by_id(str(chunk_id))
            vector = self._embed(chunk.chunk_text)

            emb = Embedding(chunk_id=chunk_id, embedding=vector)
            saved = self.embedding_repository.create(emb)
            created.append(saved)

        return created

    def process_user(self, user_id: uuid.UUID):
        docs = self.document_repository.get_by_user(str(user_id))
        doc_ids = [d.id for d in docs]

        all_chunks = []
        for doc_id in doc_ids:
            chunks = self.chunk_service.create_chunks_for_document(doc_id)
            all_chunks.extend(chunks)

        chunk_ids = [c.id for c in all_chunks]
        embeddings = self.create_embeddings_for_chunks(chunk_ids)

        return {
            "documents_processed": len(doc_ids),
            "chunks_created": len(all_chunks),
            "embeddings_created": len(embeddings),
        }
