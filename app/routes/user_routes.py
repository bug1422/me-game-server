from flask_bcrypt import Bcrypt
from flask import request, Blueprint, jsonify, current_app, g
from flasgger import swag_from
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.dtos.user import UserOutputDTO
from app.tools.response import Response
from app.dtos.response import ResponseDTO

user_routes = Blueprint("user_routes", __name__)


@user_routes.before_request
def before_request():
    g.bcrypt = Bcrypt(current_app)
    g.user_repo = UserRepository()
    g.user_service = UserService(g.user_repo, g.bcrypt)


@user_routes.get("/get-by-email/<email>")
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "email",
                "in": "path",
                "description": "User email",
                "required": True,
                "type": "string",
            }
        ],
        "responses": {"200": {"description": "get test"}},
    }
)
def get_user_by_email(email):
    res: Response = g.user_service.get_user_by_email(email)
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, UserOutputDTO), 200


@user_routes.get("/get-by-id/<id>")
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string",
            }
        ],
        "responses": {
            "200": {"description": "get test"},
            "404": {"description": "User not found"},
        },
    }
)
def get_user_by_id(id):
    res: Response = g.user_service.get_user_by_id(id)
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, UserOutputDTO), 200


@user_routes.post("/")
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "user",
                "in": "body",
                "description": "User data",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "nickname": {"type": "string"},
                        "email": {"type": "string"},
                        "password": {"type": "string"},
                    },
                    "example": {
                        "name": "john_doe",
                        "nickname": "johnny",
                        "email": "john@example.com",
                        "password": "123",
                    },
                },
            }
        ],
        "responses": {
            "201": {
                "description": "User created successfully",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "user_id": {"type": "integer"},
                            },
                            "example": {
                                "message": "User created successfully",
                                "user_id": 1234,
                            },
                        }
                    }
                },
            },
            "400": {"description": "Invalid data"},
        },
    }
)
def create_user():
    data = request.get_json()
    res: Response = g.user_service.create_user(
        data["name"], data["nickname"], data["email"], data["password"]
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, UserOutputDTO), 200


@user_routes.put("/")
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "user",
                "in": "body",
                "description": "User data",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "required": True,
                        },
                        "name": {"type": "string"},
                        "nickname": {"type": "string"},
                        "password": {"type": "string"},
                    },
                },
                "example": {
                    "id": "ALJBLKCUIO123",
                    "name": "john_doe",
                    "nickname": "johnny",
                    "password": "123",
                },
            }
        ],
    }
)
def update_user():
    data = request.get_json()
    res: Response = g.user_service.update_user(
        data["id"], data["name"], data["nickname"], data["password"]
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, UserOutputDTO), 200
