from marshmallow import Schema, fields, validate, post_dump, EXCLUDE
from app.models.game import GamePlatform
from app.tools.custom_fields import GridFSField
from app.dtos.voter import VoterOutputDTO
from app.dtos.comment import CommentOutputDto

class GameInputDTO(Schema):
    publisher_id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    embedded_link = fields.String(required=False)
    ref_link = fields.String(required=False)
    game_engine = fields.String(required=True)
    game_content = fields.Field(
        metadata={"type": "string", "format": "byte"}, allow_none=True
    )
    platform = fields.Enum(GamePlatform, required=True)
    tags = fields.List(fields.String())
    thumbnail = fields.Field(
        metadata={"type": "string", "format": "byte"}, allow_none=False
    )

class GameChangeLogInputDTO(Schema):
    version = fields.String(required=True,validate=validate.Regexp(r'^\d+\.\d+\.\d+$',error='The version must follow the format X.Y.Z'))
    log = fields.String(required=False)
    class Meta:
        unknown = EXCLUDE

class GameChangeLogOutputDTO(Schema):
    major = fields.Integer()
    minor = fields.Integer()
    patch = fields.Integer()
    log = fields.String()

    @post_dump
    def combine_version_string(self, data, **kwargs):
        return {
            "version": f"{data['major']}.{data['minor']}.{data['patch']}",
            "log": f"{data['log']}"
            }

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
    ref_link = fields.String()
    game_content = GridFSField()
    change_logs = fields.List(fields.Nested(GameChangeLogOutputDTO))
    comments = fields.List(fields.Nested(CommentOutputDto))


class GamePagingDTO(Schema):
    game_list = fields.List(fields.Nested(GameThumbnailOutputDTO))
    current_page = fields.Int()
    max_page = fields.Int()
