from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_session
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)


@router.post("/")
def create_user(
    username: str,
    name: str = None,
    bio: str = None,
    avatar_url: str = None,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(username, name, bio, avatar_url)


@router.get("/")
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.get("/{user_id}")
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)
