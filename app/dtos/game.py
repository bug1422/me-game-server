from marshmallow import Schema, fields
from app.models.game import GamePlatform
from app.tools.custom_fields import GridFSField
from app.dtos.voter import VoterOutputDTO


class GameInputDTO(Schema):
    publisher_id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    embedded_link = fields.String(required=True)
    game_engine = fields.String(required=True)
    game_content = fields.Field(
        metadata={"type": "string", "format": "byte"}, allow_none=True
    )
    platform = fields.Enum(GamePlatform, required=True)
    tags = fields.List(fields.String())
    thumbnail = fields.Field(
        metadata={"type": "string", "format": "byte"}, allow_none=False
    )


class GameThumbnailOutputDTO(Schema):
    id = fields.String()
    publisher_id = fields.String()
    title = fields.String()
    description = fields.String()
    tags = fields.List(
        fields.String(),
    )
    game_engine = fields.String()
    upvote = fields.Int()
    downvote = fields.Int()
    played_count = fields.Int()
    created_at = fields.DateTime()
    thumbnail = GridFSField()


class GameDetailOutputDTO(Schema):
    id = fields.String()
    publisher_id = fields.String()
    title = fields.String()
    description = fields.String()
    tags = fields.List(
        fields.String(),
    )
    game_engine = fields.String()
    upvote = fields.Number()
    downvote = fields.Number()
    upvote_list = fields.List(fields.Nested(VoterOutputDTO))
    downvote_list = fields.List(fields.Nested(VoterOutputDTO))
    played_count = fields.Number()
    created_at = fields.DateTime()
    embedded_link = fields.String()
    game_content = GridFSField()


class GamePagingDTO(Schema):
    game_list = fields.List(fields.Nested(GameThumbnailOutputDTO))
    current_page = fields.Int()
    max_page = fields.Int()
