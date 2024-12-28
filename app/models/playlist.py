import mongoengine as me
from datetime import datetime, timezone


class Playlist(me.Document):
    games = me.ListField(me.ReferenceField("Game"))
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
