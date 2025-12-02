import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domains.users.service import UserService
from app.domains.users.languages_service import UserLanguagesService
from app.infrastructure.github.github_info_service import GithubInfoService
from app.domains.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(
    username: str,
    name: str,
    bio: str,
    avatar_url: str,
    github_username: str,
    session: Session = Depends(get_session),
):
    # Added: inject session into UserService
    service = UserService(session)
    return service.create_user(username, name, bio, avatar_url, github_username)


@router.get("/", response_model=list[User])
def list_users(session: Session = Depends(get_session)):
    service = UserService(session)
    return service.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_user(user_id)


@router.get("/github/info/{username}")
async def extract_info_github(username: str, session: Session = Depends(get_session)):
    # Added: shared session for user lookup
    user_service = UserService(session)
    github_service = GithubInfoService()

    internal_user = user_service.get_user_by_github(username)
    if not internal_user:
        raise HTTPException(404, "Internal user not found")

    return await github_service.extract(
        username=username, internal_user_id=str(internal_user.id)
    )


@router.post("/{user_id}/languages/save")
def save_user_languages(
    user_id: str,
    session: Session = Depends(get_session),
):
    user_service = UserService(session)

    if not user_service.get_user_by_id(id=user_id):
        raise HTTPException(404, "Internal user not found")

    lang_service = UserLanguagesService(session)
    result = lang_service.save_user_languages(uuid.UUID(user_id))

    return {"saved": len(result)}


@router.delete("/all/{user_id}")
def delete_user_all_information(
    user_id: str,
    session: Session = Depends(get_session),
):
    user_service = UserService(session)
    user_service.delete_user_data(uuid.UUID(user_id))

    return {"deleted": True}
