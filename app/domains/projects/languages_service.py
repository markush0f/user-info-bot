import os
import json
import uuid
from app.core.db import get_session
from app.domains.projects.models.project_language import ProjectLanguage
from app.infrastructure.repositories.project_language_repository import ProjectLanguagesRepository
from app.infrastructure.repositories.project_repository import ProjectRepository


class ProjectLanguagesService:
    def __init__(self, session):
        self.session = session
        self.repo = ProjectLanguagesRepository(self.session)
        self.projects = ProjectRepository(self.session)

    # Save languages for a single project
    def save_single_project_languages(self, project_id: str):
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
                project_id=uuid.UUID(project_id),
                language=lang,
                bytes=bytes_value
            )
            saved.append(self.repo.create(item))

        return saved

    # Save languages for all or selected projects
    def save_multiple_projects_languages(self, user_id: str, selection):
        if selection == "all":
            projects = self.projects.get_all(user_id)
        else:
            projects = [self.projects.get_by_id(pid) for pid in selection]

        total_saved = 0

        for project in projects:
            if not project:
                continue

            saved = self.save_single_project_languages(str(project.id))
            total_saved += len(saved)

        self.session.close()
        return total_saved
