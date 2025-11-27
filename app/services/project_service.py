import uuid
from app.db import get_session
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.services.summary_projects_service import SummaryProjectsService
from app.utils.file_writer import save_text
from app.utils.github_files_loader import extract_projects
from app.logger import logger

class ProjectService:
    # Opens a session and initializes the repository
    def __init__(self):
        self.session = get_session()
        self.repository = ProjectRepository(self.session)
        self.summarizer = SummaryProjectsService()

    # Creates a project or returns it if it already exists
    def create_project(
        self,
        user_id: uuid.UUID,
        repo_name: str,
        description: str,
        stars: int,
        forks: int,
        last_commit: str,
    ):

        existing = self.repository.get_by_name(user_id, repo_name)
        if existing:
            self.session.close()
            return existing

        project = Project(
            user_id=user_id,
            repo_name=repo_name,
            description=description,
            stars=stars,
            forks=forks,
            last_commit=last_commit,
        )

        result = self.repository.create(project)
        self.session.close()
        return result

    # Retrieves a project by ID
    def get_project(self, project_id: str):
        result = self.repository.get_by_id(project_id)
        self.session.close()
        return result

    # Retrieves multiple projects, optionally filtered by user
    def list_projects(self, user_id: str):
        result = self.repository.get_all(user_id)
        self.session.close()
        return result

    # Updates one project
    def update_project(self, project_id: str, **fields):
        project = self.repository.get_by_id(project_id)
        if not project:
            self.session.close()
            return None

        for key, value in fields.items():
            setattr(project, key, value)

        result = self.repository.update(project)
        self.session.close()
        return result

    # Deletes one project
    def delete_project(self, project_id: str):
        result = self.repository.delete(project_id)
        self.session.close()
        return result

    # Added: summarize one project
    def summarize_single_project(self, project: dict):
        logger.info(f"Summarizing single project: {project.get('name')}")

        content = f"""
        Project name: {project.get('name')}
        Description: {project.get('description')}
        Languages: {project.get('languages')}
        Commit count: {project.get('commit_count')}
        README:
        {project.get('readme', '')}
        """
        summary = self.summarizer.summarize_project(content)
        logger.debug(f"Summary created for project: {project.get('name')}")
        return summary

    # Added: summarize all projects and save output
    def summarize_all_projects(self):
        logger.info("Loading all extracted projects")
        projects = extract_projects("output")

        for project in projects:
            name = project["name"]
            logger.info(f"Summarizing project: {name}")

            summary = self.summarize_single_project(project)

            summary_path = f"output/projects/{name}/summary.txt"
            save_text(summary, summary_path) # type: ignore

            logger.debug(f"Summary saved at: {summary_path}")

        logger.info("All project summaries generated successfully")
        return True
