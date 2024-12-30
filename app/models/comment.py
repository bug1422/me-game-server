import mongoengine as me
from bson import ObjectId
from datetime import datetime, timezone
from app.models.voter import Voter


class Comment(me.EmbeddedDocument):
    content = me.StringField()
    user_id = me.ObjectIdField(required=True)
    upvote = me.IntField(min_value=0, default=0)
    upvote_list = me.EmbeddedDocumentListField(Voter, default=[])
    downvote = me.IntField(min_value=0, default=0)
    downvote_list = me.EmbeddedDocumentListField(Voter, default=[])
    sub_thread_count = me.IntField(0, default=0)
    parent_id = me.ReferenceField("Comment")
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
    removed_at = me.DateTimeField(required=False, default=None)
