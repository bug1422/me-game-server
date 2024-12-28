import mongoengine as me
from enum import Enum
from datetime import datetime, timezone


class ReportType(Enum):
    BUG = "bug"
    LEGAL = "legal"
    SUGGEST = "suggest"


class ReportStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPELTED = "completed"


class Report(me.Document):
    ticket_code = me.StringField()
    game = me.ReferenceField("Game")
    sender = me.ReferenceField("User")
    type = me.EnumField(ReportType)
    status = me.EnumField(ReportStatus, default=ReportStatus.PENDING)
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    removed_at = me.DateTimeField(required=False, default=None)
    meta = {"collection": "report"}
