from app.models.embbeding import Embedding
from sqlalchemy import text  

class EmbeddingRepository:
    def __init__(self, session):
        self.session = session

    def create(self, item: Embedding):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_chunk_ids(self, chunk_ids):
        if not chunk_ids:
            return
        self.session.execute(
            text("DELETE FROM embeddings WHERE chunk_id = ANY(:ids)"),  
            {"ids": chunk_ids}
        )
        self.session.commit()

    def get_by_id(self, entity_id: str):
        return self.session.get(Embedding, entity_id)
