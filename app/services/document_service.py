import uuid
from app.db import get_session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.repositories.entity_repository import EntityRepository
from app.services.document_builder_service import DocumentBuilderService


class DocumentService:
    def __init__(self):
        self.session = get_session()
        self.repo = DocumentRepository(self.session)
        self.entity_repo = EntityRepository(self.session)
        self.builder = DocumentBuilderService()

    def generate_document(self, entity_id: uuid.UUID):
        entity = self.entity_repo.get_by_id(str(entity_id))
        if not entity:
            self.session.close()
            return None

        entity_dict = {
            "id": str(entity.id),
            "type": entity.type,
            "summary": entity.summary,
            "raw_data": entity.raw_data,
        }

        title, content = self.builder.build_document(entity_dict)

        document = Document(entity_id=entity.id, title=title, content=content)

        saved = self.repo.create(document)
        self.session.close()
        return saved
