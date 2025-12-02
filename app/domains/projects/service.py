import uuid
from app.domains.documents.service import DocumentService
from app.domains.projects.models.project import Project
from app.infrastructure.repositories.entity_repository import EntityRepository
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.domains.entities.service import EntityService
from app.domains.projects.summary_service import SummaryProjectsService
from app.shared.utils.file_writer import save_text
from app.infrastructure.github.github_files_loader import (
    extract_projects,
    extract_summaries,
)
from app.core.logger import logger


class ProjectService:
    def __init__(self, session):
        self.session = session
        self.project_repository = ProjectRepository(self.session)
        self.entity_repository = EntityRepository(self.session)
        self.summarizer = SummaryProjectsService()
        self.entity_service = EntityService(self.session)
        self.document_service = DocumentService(self.session)

    def create_project(
        self,
        user_id: uuid.UUID,
        repo_name: str,
        description: str,
        stars: int,
        forks: int,
        last_commit: str,
    ):
        data = {
            "description": description,
            "stars": stars,
            "forks": forks,
            "last_commit": last_commit,
        }

        project = self._upsert_project(user_id, repo_name, data)
        self.session.commit()
        return project

    # Retrieves a project by ID
    def get_project(self, project_id: str):
        result = self.project_repository.get_by_id(project_id)
        return result

    # Retrieves multiple projects, optionally filtered by user
    def list_projects(self, user_id: str):
        result = self.project_repository.get_all(user_id)
        return result

    # Updates one project
    def update_project(self, project_id: str, **fields):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            return None

        for key, value in fields.items():
            setattr(project, key, value)

        result = self.project_repository.update(project)
        self.session.commit()
        return result

    # Deletes one project
    def delete_project(self, project_id: str):
        result = self.project_repository.delete(project_id)
        self.session.commit()
        return result

    def summarize_all_projects(self):
        return self.summarizer.summarize_all_projects()

    # Save selected projects + entities
    def save_all_projects(self, selection):
        logger.info("Loading project data from output")

        projects = extract_projects("output")
        results = []

        if selection != "all":
            projects = [p for p in projects if p["name"] in selection]

        for project in projects:
            logger.info(f"Saving project: {project['name']}")

            project_row = self._save_project_record(project)

            entity_row = self.entity_service.create_entity(
                user_id=project_row.user_id,
                project_id=project_row.id,
                entity_type="project_summary",
                raw_data={
                    "project": project,
                },
                summary=project.get("summary"),
            )

            document_row = self.document_service.generate_document(entity_row)

            results.append(
                {
                    "project_id": project_row.id,
                    "entity_id": entity_row.id,
                    "document_id": document_row.id,
                }
            )
            
        self.session.commit()
        
        return {"saved": results}

    def delete_all(self, user_id):
        self.project_repository.delete_all_by_user(user_id)

    def _save_project_record(self, project: dict):
        return self._upsert_project(
            user_id=project["user_id"], repo_name=project["name"], data=project
        )

    def _upsert_project(self, user_id: uuid.UUID, repo_name: str, data: dict):
        # Added: unified method for create or get existing project
        existing = self.project_repository.get_by_name(user_id, repo_name)
        if existing:
            return existing

        project = Project(
            user_id=user_id,
            repo_name=repo_name,
            description=data.get("description", ""),
            stars=data.get("stars", 0),
            forks=data.get("forks", 0),
            last_commit=data.get("last_commit"),
        )

        self.project_repository.create(project)
        return project
