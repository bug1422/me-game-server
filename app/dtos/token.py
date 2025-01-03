from marshmallow import Schema, fields, EXCLUDE


class JwtTokenOutputDTO:
    access_token = fields.String()


class JwtTokenInputDTO(Schema):
    id = fields.String()
    email = fields.String()
    name = fields.String()
    exp_date = fields.DateTime()
    class Meta:
        unknown = EXCLUDE
