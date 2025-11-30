import uuid
from openai import OpenAI
from app.core.db import get_session
from app.domains.embeddings.models.embbeding import Embedding
from app.domains.documents.repository import DocumentRepository
from app.infrastructure.repositories.chunk_repository import ChunkRepository
from app.domains.chunks.service import ChunkService
from app.core.logger import logger
from app.infrastructure.repositories.embedding_repository import EmbeddingRepository  


class EmbeddingService:
    def __init__(self):
        self.session = get_session()
        self.document_repository = DocumentRepository(self.session)
        self.chunk_repository = ChunkRepository(self.session)
        self.embedding_repository = EmbeddingRepository(self.session)
        self.chunk_service = ChunkService()
        self.client = OpenAI()
        logger.info("EmbeddingService initialized")  

    def _embed(self, text: str):
        logger.debug("Requesting embedding")  
        response = self.client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding

    def create_embeddings_for_chunks(self, chunk_ids: list[uuid.UUID]):
        logger.info(f"Creating embeddings for {len(chunk_ids)} chunks")  
        created = []

        for chunk_id in chunk_ids:
            chunk = self.chunk_repository.get_by_id(str(chunk_id))
            logger.debug(f"Embedding chunk {chunk_id}")  

            vector = self._embed(chunk.chunk_text)

            emb = Embedding(chunk_id=chunk_id, embedding=vector)
            saved = self.embedding_repository.create(emb)

            logger.debug(f"Saved embedding {saved.id} for chunk {chunk_id}")  
            created.append(saved)

        logger.info(f"Created {len(created)} embeddings")  
        return created

    def process_user(self, user_id: uuid.UUID):
        logger.info(f"Processing embeddings for user {user_id}")  

        docs = self.document_repository.get_by_user(str(user_id))
        doc_ids = [d.id for d in docs]
        logger.info(f"Found {len(doc_ids)} documents for user {user_id}")  

        all_chunks = []
        for doc_id in doc_ids:
            logger.info(f"Creating chunks for document {doc_id}")  
            chunks = self.chunk_service.create_chunks_for_document(doc_id)
            all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} chunks for user {user_id}")  

        chunk_ids = [c.id for c in all_chunks]
        embeddings = self.create_embeddings_for_chunks(chunk_ids)

        logger.info(f"Created embeddings for user {user_id}")  

        return {
            "documents_processed": len(doc_ids),
            "chunks_created": len(all_chunks),
            "embeddings_created": len(embeddings),
        }
