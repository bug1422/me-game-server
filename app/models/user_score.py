import mongoengine as me
from datetime import datetime, timezone


class UserScore(me.EmbeddedDocument):
    user_id = me.ObjectIdField(required=True)
    user_nickname = me.StringField()
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    score = me.IntField(0)
    meta = {"collection": "score"}
