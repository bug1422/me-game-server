from app.repositories.base_repository import BaseRepository
from app.models.user import User
from mongoengine import Q


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> User:
        return User.objects(email=email).first()

    def get_by_email_or_nickname(self, identifier: str) -> User:
        return User.objects(Q(email=identifier) | Q(nickname=identifier)).first()
