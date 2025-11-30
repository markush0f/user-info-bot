from sqlalchemy import text

from app.domains.documents.models.document import Document  


class DocumentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, doc: Document):
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)
        return doc

    def get_by_id(self, entity_id: str):
        return self.session.get(Document, entity_id)

    def get_by_user(self, user_id):
        query = text(  
            """
            SELECT d.*
            FROM documents d
            JOIN entities e ON e.id = d.entity_id
            WHERE e.user_id = :u
            """
        )

        rows = self.session.execute(query, {"u": user_id})
        return [Document.model_validate(row) for row in rows]
