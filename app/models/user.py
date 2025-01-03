import mongoengine as me
from datetime import datetime, timezone


class User(me.Document):
    name = me.StringField()
    nickname = me.StringField(unique=True)
    email = me.StringField(unique=True)
    password = me.StringField()
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
    meta = {"collection": "user"}
