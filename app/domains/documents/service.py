from typing import List
import uuid
from app.domains.documents.models.document import Document
from app.domains.documents.repository import DocumentRepository
from app.domains.documents.builder_service import DocumentBuilderService
from app.shared.services.record_finder import RecordFinder


class DocumentService:
    def __init__(self, session):
        self.session = session
        self.document_repository = DocumentRepository(self.session)
        self.builder = DocumentBuilderService()
        self.record_finder = RecordFinder(repo=self.document_repository)

    def generate_document(self, entity):
        entity_dict = {
            "id": str(entity.id),
            "type": entity.type,
            "summary": entity.summary,
            "raw_data": entity.raw_data,
        }

        title, content = self.builder.build_document(entity_dict)
        document = Document(entity_id=entity.id, title=title, content=content)

        return self.document_repository.create(document)

    def get_by_id(self, id: uuid.UUID):
        return self.record_finder.find_or_404(record_id=id)

    def get_by_user_id(self, user_id: uuid.UUID) -> List[Document]:
        return self.document_repository.get_by_user(user_id)

    def delete_all(self, user_id):
        self.document_repository.delete_all_by_user(user_id)
