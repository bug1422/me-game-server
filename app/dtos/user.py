from marshmallow import Schema, fields


class UserOutputDTO(Schema):
    id = fields.Str()
    name = fields.Str()
    nickname = fields.Str()
    email = fields.Email()
