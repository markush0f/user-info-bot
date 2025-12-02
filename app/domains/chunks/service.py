from app.infrastructure.repositories.chunk_repository import ChunkRepository
from app.domains.chunks.models.chunk import Chunk
from app.core.logger import logger


class ChunkService:
    def __init__(self, session):
        self.session = session
        self.chunk_repository = ChunkRepository(self.session)

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

    def create_chunks_for_document(self, document):
        document_id = document.id
        logger.info(f"Processing document {document_id}")

        self.chunk_repository.delete_by_document(document_id)

        parts = self._split(document.content)

        created = []
        for idx, text in enumerate(parts):
            chunk = Chunk(document_id=document_id, chunk_index=idx, chunk_text=text)
            created.append(self.chunk_repository.create(chunk))
            
        self.session.commit()
        return created

    def delete_all(self, user_id):
        self.chunk_repository.delete_all_by_user(user_id)
        self.session.commit()
        
    def get_by_id(self, id)-> Chunk:
        return self.chunk_repository.get_by_id(id)