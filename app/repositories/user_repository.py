from sqlmodel import Session, select
from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id):
        return self.session.get(User, user_id)

    def get_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def get_all(self):
        statement = select(User)
        return self.session.exec(statement).all()
