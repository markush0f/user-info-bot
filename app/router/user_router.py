from fastapi import APIRouter
from app.services.github_info_service import GithubInfoService
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(
    username: str,
    name: str,
    bio: str,
    avatar_url: str,
    github_username: str,
):
    service = UserService()
    return service.create_user(username, name, bio, avatar_url, github_username)


@router.get("/", response_model=list[User])
def list_users():
    service = UserService()
    return service.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    service = UserService()
    return service.get_user(user_id)

@router.get("/github/info/{username}")
async def  extract_info_github(username: str):
    service = GithubInfoService()
    return await service.extract(username)