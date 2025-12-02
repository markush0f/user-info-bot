import uuid
from sqlmodel import Session, select
from sqlalchemy import text
from app.domains.projects.models.project import Project


class ProjectRepository:
    model_name = "Project"

    def __init__(self, session: Session):
        self.session = session

    def create(self, project: Project):
        self.session.add(project)
        return project

    def get_by_id(self, project_id: str):
        return self.session.get(Project, project_id)

    def get_by_name(self, user_id: uuid.UUID, repo_name: str):
        statement = select(Project).where(
            Project.user_id == user_id, Project.repo_name == repo_name
        )
        return self.session.exec(statement).first()

    def get_all(self, user_id: str):
        if user_id:
            statement = select(Project).where(Project.user_id == user_id)
        else:
            statement = select(Project)
        return self.session.exec(statement).all()

    def update(self, project: Project):
        self.session.add(project)
        return project

    def delete(self, project_id: str):
        project = self.session.get(Project, project_id)
        if project:
            self.session.delete(project)
        return project

    def delete_all_by_user(self, user_id: uuid.UUID):
        sql = text(
            """
            DELETE FROM projects
            WHERE user_id = :user_id
        """
        )
        self.session.execute(sql, {"user_id": user_id})
