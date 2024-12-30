from typing import TypeVar, Type
from app.tools.response import Response
from marshmallow import Schema, fields

T = TypeVar("T", bound=Schema)


class ResponseDTO:
    def __init__(self, message, is_success, response):
        self.message = message
        self.is_success = is_success
        self.response = response

    @classmethod
    def convert(cls, response: Response, schema: Type[T] = None):
        if schema:
            mapped = schema().dump(response.response)
            return ResponseDTO(response.message, response.result, mapped).to_dict()
        else:
            return ResponseDTO(response.message, response.result, None).to_dict()

    def to_dict(self):
        return {
            "message": self.message,
            "is_success": self.is_success,
            "response": self.response,
        }
