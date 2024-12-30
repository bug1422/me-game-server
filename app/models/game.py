import mongoengine as me
from enum import Enum
from datetime import datetime, timezone
from app.models.voter import Voter
from app.models.comment import Comment
from app.models.user_score import UserScore


class GamePlatform(Enum):
    ITCH = "ITCH"
    OTHER = "OTHER"


class Game(me.Document):
    publisher = me.ReferenceField("User")
    platform = me.EnumField(GamePlatform, default=GamePlatform.ITCH)
    game_engine = me.StringField(required=True)
    title = me.StringField()
    description = me.StringField()
    tags = me.ListField(me.StringField())
    upvote = me.IntField(min_value=0, default=0)
    upvote_list = me.EmbeddedDocumentListField(Voter, default=[])
    downvote = me.IntField(min_value=0, default=0)
    downvote_list = me.EmbeddedDocumentListField(Voter, default=[])
    played_count = me.IntField(0, default=0)
    comments = me.EmbeddedDocumentListField(Comment, default=[])
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    is_hidden = me.BooleanField(default=False)
    scores = me.EmbeddedDocumentListField(UserScore, default=[])
    removed_at = me.DateTimeField(required=False, default=None)
    embedded_link = me.StringField(required=False, default=None)
    thumbnail = me.FileField(collection_name="image")
    game_content = me.FileField(collection_name="game_content")
    meta = {"collection": "game"}
