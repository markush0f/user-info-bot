from app.models.project_language import ProjectLanguage


class ProjectLanguagesRepository:
    def __init__(self, session):
        self.session = session

    def create(self, item: ProjectLanguage):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
