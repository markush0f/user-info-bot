import uuid
import json
from app.domains.users.models.user_language import UserLanguage
from app.infrastructure.repositories.user_languages_repository import UserLanguagesRepository


class UserLanguagesService:
    def __init__(self, session):
        self.session = session
        self.repo = UserLanguagesRepository(self.session)

    def save_user_languages(self, user_id: uuid.UUID):
        # Load languages file from local
        path = "output/languages/top_languages.json"
        with open(path, "r", encoding="utf-8") as f:
            languages = json.load(f)

        saved = []

        for lang, bytes_value in languages.items():
            item = UserLanguage(
                user_id=user_id, language=lang, bytes=bytes_value, repos_count=None
            )
            saved.append(self.repo.create(item))

        self.session.close()
        return saved
