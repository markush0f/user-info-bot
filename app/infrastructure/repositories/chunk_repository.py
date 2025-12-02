import uuid
from sqlalchemy import text
from app.domains.chunks.models.chunk import Chunk


class ChunkRepository:
    model_name = "Chunk"

    def __init__(self, session):
        self.session = session

    def create(self, chunk: Chunk):
        self.session.add(chunk)
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

    def get_by_id(self, entity_id: str):
        return self.session.get(Chunk, entity_id)

    def delete_all_by_user(self, user_id: uuid.UUID):
        sql = text(
            """
            DELETE FROM chunks
            USING documents, entities
            WHERE chunks.document_id = documents.id
            AND documents.entity_id = entities.id
            AND entities.user_id = :user_id
        """
        )
        self.session.execute(sql, {"user_id": user_id})
