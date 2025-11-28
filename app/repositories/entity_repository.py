from app.models.entity import Entity

class EntityRepository:
    def __init__(self, session):
        self.session = session

    def create(self, data: dict):
        entity = Entity(**data)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_project(self, project_id):
        return (
            self.session.query(Entity)
            .filter(Entity.project_id == project_id)
            .first()
        )

    def get_by_id(self, entity_id: str):
        return self.session.get(Entity, entity_id)