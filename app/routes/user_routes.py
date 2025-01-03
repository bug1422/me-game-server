from flask import request, Blueprint, jsonify, g
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required
from flasgger import swag_from
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.dtos.user import UserOutputDTO
from app.tools.response import Response
from app.dtos.response import ResponseDTO
from app.dtos.token import JwtTokenInputDTO

user_routes = Blueprint("user_routes", __name__)


@user_routes.before_request
def before_request():
    g.user_repo = UserRepository()
    from app import bcrypt

    g.user_service = UserService(g.user_repo, bcrypt)


@user_routes.get("/test-jwt")
@swag_from(
    {
        "tags": ["Tets"],
        "responses": {"200": {"description": "get test"}},
    }
)
@jwt_required()
def get_claims_in_jwt():
    claims = get_jwt()
    token = JwtTokenInputDTO().load(claims)
    return jsonify(token), 200

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
        "responses": {"200": {"description": "get"}},
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


@user_routes.get("/login")
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {"name": "identifier", "in": "query", "required": True, "type": "string"},
            {"name": "password", "in": "query", "required": True, "type": "string"},
        ],
        "responses": {
            "200": {"description": "get test"},
            "404": {"description": "User not found"},
        },
    }
)
def login():
    res: Response = g.user_service.login(
        request.args.get("identifier"), request.args.get("password")
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return jsonify(res.response)


@user_routes.post("/register")
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
    return jsonify(res.response)


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
