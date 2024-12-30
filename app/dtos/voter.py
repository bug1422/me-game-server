from marshmallow import Schema, fields


class VoterOutputDTO(Schema):
    user_id = fields.String()
    user_nickname = fields.String()
    created_at = fields.DateTime()
