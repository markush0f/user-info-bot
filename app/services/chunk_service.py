import uuid
from app.db import get_session
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.models.chunk import Chunk
from app.logger import logger


class ChunkService:
    def __init__(self):
        self.session = get_session()
        self.documents = DocumentRepository(self.session)
        self.chunks = ChunkRepository(self.session)
        logger.info("ChunkService initialized")

    def _split(self, text: str, max_tokens: int = 300):
        words = text.split()
        parts = []
        current = []

        for w in words:
            current.append(w)
            if len(current) >= max_tokens:
                parts.append(" ".join(current))
                current = []

        if current:
            parts.append(" ".join(current))

        logger.debug(f"Split text into {len(parts)} chunks")
        return parts

    def create_chunks_for_document(self, document_id: uuid.UUID):
        logger.info(f"Processing document {document_id}")

        doc = self.documents.get_by_id(str(document_id))
        if not doc:
            logger.warning(f"Document {document_id} not found")
            self.session.close()
            return []

        self.chunks.delete_by_document(document_id)
        logger.info(f"Deleted previous chunks for document {document_id}") 
        parts = self._split(doc.content)

        created = []
        for idx, text in enumerate(parts):
            chunk = Chunk(document_id=document_id, chunk_index=idx, chunk_text=text)
            created_chunk = self.chunks.create(chunk)
            created.append(created_chunk)
            logger.debug(f"Created chunk {created_chunk.id} index {idx}")

        logger.info(f"Created {len(created)} chunks for document {document_id}")
        return created
