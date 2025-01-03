import mongoengine as me
from enum import Enum
from datetime import datetime, timezone
from app.models.voter import Voter
from app.models.comment import Comment
from app.models.user_score import UserScore


class GamePlatform(Enum):
    ITCH = "ITCH"
    OTHER = "OTHER"


class GameChangeLog(me.EmbeddedDocument):
    major = me.IntField(min_value=0, default=1)
    minor = me.IntField(min_value=0, default=0)
    patch = me.IntField(min_value=0, default=0, unique_with=["major", "minor"])
    log = me.StringField(required=False)


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
    change_logs = me.EmbeddedDocumentListField(GameChangeLog, default=[])
    meta = {"collection": "game"}

    def add_change_log(self, major, minor, patch, log: str):
        for change_log in self.change_logs:
            if change_log.major == major and change_log.minor == minor and change_log.patch == patch:
                raise me.ValidationError(f"This version {major}.{minor}.{patch} has already existed")
            elif (
                change_log.major > major
                or (change_log.major == major and change_log.minor > minor)
                or (change_log.minor == major and change_log.minor == minor and change_log.patch > patch)
            ):
                raise me.ValidationError(f"This version {major}.{minor}.{patch} isn't the latest")
        print(log)
        self.change_logs.append(GameChangeLog(major=major, minor=minor, patch=patch, log=log))
        self.save()
