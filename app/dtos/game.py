from marshmallow import Schema, fields
from app.models.game import GamePlatform
from app.tools.custom_fields import GridFSField


class GameInputDTO(Schema):
    publisher_id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    embedded_link = fields.String(required=True)
    platform = fields.Enum(GamePlatform, required=True)
    tags = fields.List(fields.String())
    thumbnail = fields.Field(
        metadata={"type": "string", "format": "byte"}, allow_none=True
    )


class GameOutputDTO(Schema):
    publisher_id = fields.String()
    title = fields.String()
    description = fields.String()
    tags = fields.List(
        fields.String(),
    )
    upvote = fields.Number()
    downvote = fields.Number()
    played_count = fields.Number()
    created_at = fields.DateTime()
    embedded_link = fields.String()
    thumbnail = GridFSField()
