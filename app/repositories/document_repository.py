from app.models.document import Document

class DocumentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, doc: Document):
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)
        return doc
