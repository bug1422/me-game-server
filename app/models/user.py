import mongoengine as me
from datetime import datetime, timezone
from enum import Enum


class UserRole(Enum):
    MEMBER = "member"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(me.Document):
    name = me.StringField()
    nickname = me.StringField(unique=True)
    email = me.StringField(unique=True)
    password = me.StringField()
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
    meta = {"collection": "user"}
    roles = me.ListField(me.EnumField(UserRole), default=[])

    def add_role(self, role):
        if any(role == added_role.value for added_role in self.roles):
            raise Exception("User already have this role")
        self.roles.append(UserRole(role))
        self.save()

    def remove_role(self, role):
        for added_role in self.roles:
            if added_role.value == role:
                self.roles.remove(added_role)
        self.save()