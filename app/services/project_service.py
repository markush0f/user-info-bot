import uuid
from app.db import get_session
from app.models.project import Project
from app.repositories.entity_repository import EntityRepository
from app.repositories.project_repository import ProjectRepository
from app.services.entity_service import EntityService
from app.services.summary_projects_service import SummaryProjectsService
from app.utils.file_writer import save_text
from app.utils.github_files_loader import extract_projects, extract_summaries
from app.logger import logger


class ProjectService:
    # Opens a session and initializes the repository
    def __init__(self):
        self.session = get_session()
        self.project_repository = ProjectRepository(self.session)
        self.entity_repository = EntityRepository(self.session)
        self.summarizer = SummaryProjectsService()
        self.entity_service = EntityService()
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

        existing = self.project_repository.get_by_name(user_id, repo_name)
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

        result = self.project_repository.create(project)
        self.session.close()
        return result

    # Retrieves a project by ID
    def get_project(self, project_id: str):
        result = self.project_repository.get_by_id(project_id)
        self.session.close()
        return result

    # Retrieves multiple projects, optionally filtered by user
    def list_projects(self, user_id: str):
        result = self.project_repository.get_all(user_id)
        self.session.close()
        return result

    # Updates one project
    def update_project(self, project_id: str, **fields):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            self.session.close()
            return None

        for key, value in fields.items():
            setattr(project, key, value)

        result = self.project_repository.update(project)
        self.session.close()
        return result

    # Deletes one project
    def delete_project(self, project_id: str):
        result = self.project_repository.delete(project_id)
        self.session.close()
        return result

    # Summarize one project
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

    # Summarize all projects and save output
    def summarize_all_projects(self):
        logger.info("Loading all extracted projects")
        projects = extract_projects("output")

        for project in projects:
            name = project["name"]
            logger.info(f"Summarizing project: {name}")

            summary = self.summarize_single_project(project)

            summary_path = f"output/projects/{name}/summary.txt"
            save_text(summary, summary_path)  # type: ignore

            logger.debug(f"Summary saved at: {summary_path}")

        logger.info("All project summaries generated successfully")
        return True

  
    # Save selected projects + entities
    def save_projects_to_db(self, selection):
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
                summary= project.get("summary")
            )

            results.append({
                "project_id": project_row.id,
                "entity_id": entity_row
            })

        return {"saved": results}

    # Create project record
    def _save_project_record(self, project: dict):
        existing = self.project_repository.get_by_name(
            project["user_id"],
            project["name"]
        )
        if existing:
            return existing

        new_project = Project(
            user_id=project["user_id"],
            repo_name=project["name"],
            description=project.get("description", ""),
            stars=project.get("stars", 0),
            forks=project.get("forks", 0),
            last_commit=project.get("last_commit")
        )

        created = self.project_repository.create(new_project)
        return created