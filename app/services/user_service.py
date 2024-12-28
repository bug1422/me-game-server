import re
from typing import List
from app.repositories.user_repository import UserRepository
from app.models.user import User
from flask_bcrypt import Bcrypt


class UserService:
    def __init__(self, user_repo: UserRepository, bcrypt: Bcrypt):
        self.user_repo = user_repo
        self.bcrypt: Bcrypt = bcrypt

    def get_user_by_id(self, id):
        return self.user_repo.get_by_id(id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repo.get_by_email(email)

    def create_user(
        self, name: str, nickname: str, email: str, password: str
    ) -> User | List[str]:
        if not re.search("^[^@]+@[^@]+\.[^@]+$", email):
            return "Invalid email address"
        elif self.user_repo.get_by_email(email):
            return "Email already exist"
        user = User(
            name=name,
            nickname=nickname,
            email=email,
            password=self.hash_password(password),
        )
        return self.user_repo.add(user)

    def update_user(self, id: str, name: str, nickname: str, password: str) -> User:
        user = self.user_repo.get_by_id(id)
        if not self.check_password(user.password, password):
            return f"Incorrect password"
        user.name = name if name else user.name
        user.nickname = nickname if nickname else user.nickname
        self.user_repo.update(user)
        return None

    def hash_password(self, password):
        return self.bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, hash, password):
        return self.bcrypt.check_password_hash(hash, password)
