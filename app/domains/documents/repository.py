import uuid
from sqlalchemy import text
from app.domains.documents.models.document import Document  

class DocumentRepository:
    def __init__(self, session):
        # Added: injected session
        self.session = session

    def create(self, doc: Document):
        # Added: removed internal commit (router will control transaction)
        self.session.add(doc)
        return doc

    def get_by_id(self, entity_id: str):
        return self.session.get(Document, entity_id)

    def get_by_user(self, user_id):
        query = text("""
            SELECT d.*
            FROM documents d
            JOIN entities e ON e.id = d.entity_id
            WHERE e.user_id = :user_id
        """)

        rows = self.session.execute(query, {"user_id": user_id})
        return rows.fetchall()

    def delete_all_by_user(self, user_id: uuid.UUID):
        sql = text("""
            DELETE FROM documents
            USING entities
            WHERE documents.entity_id = entities.id
            AND entities.user_id = :user_id
        """)
        self.session.execute(sql, {"user_id": user_id})
