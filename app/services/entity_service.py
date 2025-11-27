import uuid
from app.db import get_session
from app.repositories.entity_repository import EntityRepository
from app.logger import logger


class EntityService:
    def __init__(self):
        self.session = get_session()
        self.repository = EntityRepository(self.session)

    # Save an entity linked to a project
    def create_entity(
        self,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
        entity_type: str,
        raw_data: dict,
        summary: str
    ):
        logger.info(f"Creating entity for project: {project_id}")

        entity_data = {
            "user_id": user_id,
            "project_id": project_id,
            "type": entity_type,
            "raw_data": raw_data,
            "summary": summary
        }

        existing = self.repository.get_by_project(project_id)
        if existing:
            return existing

        created = self.repository.create(entity_data)
        return created
