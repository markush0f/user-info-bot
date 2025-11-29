from app.models.chunk import Chunk
from sqlalchemy import text  


class ChunkRepository:
    def __init__(self, session):
        self.session = session

    def create(self, chunk: Chunk):
        self.session.add(chunk)
        self.session.commit()
        self.session.refresh(chunk)
        return chunk

    def get_ids_by_document(self, document_id):
        rows = self.session.execute(
            text("SELECT id FROM chunks WHERE document_id = :d"),  
            {"d": document_id},
        )
        return [row[0] for row in rows]

    def delete_by_document(self, document_id):
        self.session.execute(
            text("DELETE FROM chunks WHERE document_id = :d"),  
            {"d": document_id},
        )
        self.session.commit()

    def get_by_id(self, entity_id: str):
        return self.session.get(Chunk, entity_id)
