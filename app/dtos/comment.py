from marshmallow import Schema, fields
from app.dtos.voter import VoterOutputDTO


class CommentInputDto(Schema):
    parent_id = fields.String(required=False)
    content = fields.String(required=True)


class CommentOutputDto(Schema):
    content = fields.String()
    sub_thread_count = fields.Number()
    parent_id = fields.String()
    upvote = fields.Number()
    downvote = fields.Number()
    upvote_list = fields.List(fields.Nested(VoterOutputDTO))
    downvote_list = fields.List(fields.Nested(VoterOutputDTO))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    removed_at = fields.DateTime()
