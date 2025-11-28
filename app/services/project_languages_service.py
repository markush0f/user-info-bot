import os
import json
import uuid
from app.db import get_session
from app.models.project_language import ProjectLanguage
from app.repositories.project_language_repository import ProjectLanguagesRepository
from app.repositories.project_repository import ProjectRepository


class ProjectLanguagesService:
    def __init__(self):
        self.session = get_session()
        self.repo = ProjectLanguagesRepository(self.session)
        self.projects = ProjectRepository(self.session)

    def save_project_languages(self, project_id: str):
        project = self.projects.get_by_id(project_id)
        if not project:
            self.session.close()
            return []

        path = f"output/projects/{project.repo_name}/languages.json"

        if not os.path.exists(path):
            self.session.close()
            return []

        with open(path, "r", encoding="utf-8") as f:
            languages = json.load(f)

        saved = []

        for lang, bytes_value in languages.items():
            item = ProjectLanguage(
                project_id=uuid.UUID(project_id), language=lang, bytes=bytes_value
            )
            saved.append(self.repo.create(item))

        self.session.close()
        return saved
