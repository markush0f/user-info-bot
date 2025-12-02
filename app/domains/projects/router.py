import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domains.projects.schemas.save_project_languages_request import (
    SaveProjectLanguagesRequest,
)
from app.domains.projects.schemas.save_project_request import SaveProjectsRequest
from app.domains.projects.languages_service import ProjectLanguagesService
from app.domains.projects.service import ProjectService
from app.domains.projects.models.project import Project

router = APIRouter(prefix="/project", tags=["projects"])


@router.post("/", response_model=Project)
def create_project(
    user_id: uuid.UUID,
    repo_name: str,
    description: str,
    stars: int,
    forks: int,
    last_commit: str,
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.create_project(
        user_id, repo_name, description, stars, forks, last_commit
    )


@router.get("/", response_model=list[Project])
def list_projects(
    user_id: str,
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.list_projects(user_id)


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: str,
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=Project)
def update_project(
    project_id: str,
    session: Session = Depends(get_session),
    **fields,
):
    service = ProjectService(session)
    return service.update_project(project_id, **fields)


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.delete_project(project_id)


@router.post("/summarize/all")
def summarize_all_projects(
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.summarize_all_projects()


@router.post("/save")
async def save_projects(
    request: SaveProjectsRequest,
    session: Session = Depends(get_session),
):
    service = ProjectService(session)

    selection = request.projects

    if not isinstance(selection, (str, list)):
        raise HTTPException(
            status_code=400,
            detail="Invalid selection type. Must be 'all' or a list of project names.",
        )

    return service.save_all_projects(selection)
    


@router.post("/single/languages")
def save_single_project_languages(
    project_id: str,
    session: Session = Depends(get_session),
):
    lang_service = ProjectLanguagesService(session)
    result = lang_service.save_single_project_languages(project_id)

    return {"saved": len(result)}


@router.post("/languages/save")
def save_project_languages(
    data: SaveProjectLanguagesRequest,
    session: Session = Depends(get_session),
):
    lang_service = ProjectLanguagesService(session)

    total_saved = lang_service.save_multiple_projects_languages(
        user_id=str(data.user_id),
        selection=data.projects,
    )

    return {"total_saved": total_saved}
