import mongoengine as me
from enum import Enum
from datetime import datetime, timezone


class GamePlatform(Enum):
    ITCH = "ITCH"
    OTHER = "OTHER"


class Game(me.Document):
    publisher = me.ReferenceField("User")
    platform = me.EnumField(GamePlatform, default=GamePlatform.ITCH)
    title = me.StringField()
    description = me.StringField()
    tags = me.ListField(me.StringField())
    upvote = me.IntField(0, default=0)
    downvote = me.IntField(0, default=0)
    played_count = me.IntField(0, default=0)
    comments = me.ListField(me.ReferenceField("Comment"))
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    is_hidden = me.BooleanField(default=False)
    playlists = me.ListField(me.ReferenceField("Playlist"))
    scores = me.ListField(me.ReferenceField("UserScore"))
    removed_at = me.DateTimeField(required=False, default=None)
    embedded_link = me.StringField(required=False, default=None)
    thumbnail = me.FileField(collection_name="image")
    meta = {"collection": "game"}
