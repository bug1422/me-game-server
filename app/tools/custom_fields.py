from marshmallow import fields
from mongoengine import GridFSProxy
import base64


class GridFSField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, GridFSProxy) and value:
            return base64.b64encode(value.read()).decode()
        return None
