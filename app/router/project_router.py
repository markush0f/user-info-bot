import uuid
from fastapi import APIRouter
from app.services.project_service import ProjectService
from app.models.project import Project

router = APIRouter(prefix="/projects", tags=["projects"])



@router.post("/", response_model=Project)
def create_project(
    user_id: uuid.UUID,
    repo_name: str,
    description: str,
    stars: int,
    forks: int,
    last_commit: str,
):
    service = ProjectService()
    return service.create_project(user_id, repo_name, description, stars, forks, last_commit)


@router.get("/", response_model=list[Project])
def list_projects(user_id: str):
    service = ProjectService()
    return service.list_projects(user_id)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str):
    service = ProjectService()
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, **fields):
    service = ProjectService()
    return service.update_project(project_id, **fields)


@router.delete("/{project_id}")
def delete_project(project_id: str):
    service = ProjectService()
    return service.delete_project(project_id)


