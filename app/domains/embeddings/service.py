import uuid
from openai import OpenAI
from app.domains.documents.service import DocumentService
from app.domains.embeddings.models.embbeding import Embedding
from app.domains.chunks.service import ChunkService
from app.core.logger import logger
from app.infrastructure.repositories.embedding_repository import EmbeddingRepository  


class EmbeddingService:
    def __init__(self, session):
        self.session = session
        self.document_service = DocumentService(self.session)
        self.embedding_repository = EmbeddingRepository(self.session)
        self.chunk_service = ChunkService(self.session)
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
            chunk = self.chunk_service.get_by_id(str(chunk_id))
            logger.debug(f"Embedding chunk {chunk_id}")  

            vector = self._embed(chunk.chunk_text)

            emb = Embedding(chunk_id=chunk_id, embedding=vector)
            saved = self.embedding_repository.create(emb)

            logger.debug(f"Saved embedding {saved.id} for chunk {chunk_id}")  
            created.append(saved)
            
        self.session.commit()
        
        logger.info(f"Created {len(created)} embeddings")  
        
        return created

    def process_user(self, user_id: uuid.UUID):
        logger.info(f"Processing embeddings for user {user_id}")  

        docs = self.document_service.get_by_user_id(user_id)
        doc_ids = [d.id for d in docs]
        logger.info(f"Found {len(doc_ids)} documents for user {user_id}")  

        all_chunks = []
        for doc_id in doc_ids:
            logger.info(f"Creating chunks for document {doc_id}")  
            chunks = self.chunk_service.create_chunks_for_document(doc_id)
            all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} chunks for user {user_id}")  
        
        self.session.commit()
        
        chunk_ids = [c.id for c in all_chunks]
        
        embeddings = self.create_embeddings_for_chunks(chunk_ids)

        logger.info(f"Created embeddings for user {user_id}")  

        return {
            "documents_processed": len(doc_ids),
            "chunks_created": len(all_chunks),
            "embeddings_created": len(embeddings),
        }

    def delete_all(self, user_id):
        self.embedding_repository.delete_all_by_user(user_id)
        self.session.commit()