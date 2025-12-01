from app.core.db import get_session
from app.domains.users.models.user import User
from app.infrastructure.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.session = get_session()
        self.repository = UserRepository(self.session)

    def create_user(self, username, name, bio, avatar_url, github_username):
        existing = self.repository.get_by_username(username)
        if existing:
            self.session.close()
            return existing

        user = User(
            username=username,
            name=name,
            bio=bio,
            avatar_url=avatar_url,
            github_username=github_username,
        )

        result = self.repository.create(user)
        self.session.close()
        return result

    def get_user(self, user_id: str):
        result = self.repository.get_by_id(user_id)
        self.session.close()
        return result

    def list_users(self):
        result = self.repository.get_all()
        self.session.close()
        return result

    def get_user_by_github(self, github_username: str):
        user = self.repository.get_by_github_username(github_username)
        self.session.close()
        return user
    
    def get_user_by_id(self, id):
        user = self.repository.get_by_id(id)
        return user