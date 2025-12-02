import uuid
from app.domains.entities.models.entity import Entity
from sqlalchemy import text

class EntityRepository:
    model_name = "Entity"

    def __init__(self, session):
        # Added: use injected session
        self.session = session

    def create(self, data: dict):
        # Added: creation without internal commit
        entity = Entity(**data)
        self.session.add(entity)
        return entity

    def get_by_project(self, project_id):
        return (
            self.session.query(Entity)
            .filter(Entity.project_id == project_id)
            .first()
        )

    def get_by_id(self, entity_id: uuid.UUID):
        return self.session.get(Entity, entity_id)

    def delete_all_by_user(self, user_id: uuid.UUID):
        # Added: delete all entities for a user
        sql = text("""
            DELETE FROM entities
            WHERE user_id = :user_id
        """)
        self.session.execute(sql, {"user_id": user_id})
