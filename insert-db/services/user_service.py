from models import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(
        self, username: str, name: str = None, bio: str = None, avatar_url: str = None
    ):
        existing = self.repository.get_by_username(username)
        if existing:
            return existing

        user = User(username=username, name=name, bio=bio, avatar_url=avatar_url)
        return self.repository.create(user)

    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)

    def list_users(self):
        return self.repository.get_all()
