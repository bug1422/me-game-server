import re
from typing import List
from app.repositories.user_repository import UserRepository
from app.models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from app.tools.response import Response
from app.tools.wrapper.handle_response import handle_response
from datetime import datetime, timezone, timedelta


class UserService:
    def __init__(self, user_repo: UserRepository, bcrypt: Bcrypt):
        self.user_repo = user_repo
        self.bcrypt: Bcrypt = bcrypt

    @handle_response
    def get_user_by_id(self, id):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise Exception("User not found")
        return user

    @handle_response
    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise Exception("User not found")
        return user

    @handle_response
    def create_user(
        self, name: str, nickname: str, email: str, password: str, roles
    ):
        if not re.search("^[^@]+@[^@]+\.[^@]+$", email):
            raise Exception("Invalid email address")
        elif self.user_repo.get_by_email(email):
            raise Exception("Email already exist")
        user = User(
            name=name,
            nickname=nickname,
            email=email,
            password=self._hash_password(password),
            roles=roles
        )
        self.user_repo.add(user)
        return self._create_access_token(user)

    @handle_response
    def add_role(
        self, user_id: str, role: str
    ):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        user.add_role(role)
        return user
    
    @handle_response
    def delete_role(
        self, user_id: str, role: str
    ):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        user.remove_role(role)
        return user

    @handle_response
    def update_user(self, id: str, name: str, nickname: str, password: str) -> User:
        user = self.user_repo.get_by_id(id)
        if not self._check_password(user.password, password):
            raise Exception("Incorrect password")
        user.name = name if name else user.name
        user.nickname = nickname if nickname else user.nickname
        self.user_repo.update(user)
        return None

    @handle_response
    def login(self, identifier: str, password: str):
        user = self.user_repo.get_by_email_or_nickname(identifier)
        if not user or not self._check_password(user.password, password):
            raise Exception("Incorrect email, nickname or password")
        return self._create_access_token(user)


    def _create_access_token(self, user):
        claims = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "exp_date": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
        }
        token = create_access_token(identity=user.id, additional_claims=claims)
        return {"access_token": token}

    def _hash_password(self, password):
        return self.bcrypt.generate_password_hash(password).decode("utf-8")

    def _check_password(self, hashed, password):
        return self.bcrypt.check_password_hash(hashed, password)
