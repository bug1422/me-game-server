import mongoengine as me
from datetime import datetime, timezone


class Comment(me.Document):
    games = me.ListField(me.ReferenceField("Game"))
    content = me.StringField()
    upvote = me.IntField(0)
    downvote = me.IntField(0)
    sub_thread_count = me.IntField(1)
    parent_comment = me.ReferenceField("self", default=None)
    replies = me.ListField(me.ReferenceField("self"))
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
    removed_at = me.DateTimeField(required=False, default=None)
