from flask import request, Blueprint, jsonify, g
from flasgger import swag_from
from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.services.game_service import GameService
from app.models.game import GamePlatform
from app.dtos.game import GameInputDTO, GameOutputDTO

game_routes = Blueprint("game_routes", __name__)


@game_routes.before_request
def before_request():
    g.game_repo = GameRepository()
    g.user_repo = UserRepository()
    g.game_service = GameService(g.game_repo, g.user_repo)


@game_routes.get("/get-all")
@swag_from(
    {
        "tags": ["Games"],
        "responses": {
            "200": {"description": "get test"},
        },
    }
)
def get_games():
    games = g.game_service.get_games()
    mapped = GameOutputDTO(many=True).dump(games)
    return mapped


@game_routes.get("/get-by-id/<id>")
@swag_from(
    {
        "tags": ["Games"],
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
def get_game_by_id(id):
    game = g.game_service.get_game_by_id(id)
    if not game:
        return jsonify({"message": "game not found"}), 404
    mapped = GameOutputDTO().dump(game)
    return mapped


@game_routes.post("/")
@swag_from(
    {
        "tags": ["Games"],
        "consumes": ["multipart/form-data", "application/json"],
        "produces": "application/json",
        "parameters": [
            {
                "name": "publisher_id",
                "in": "formData",
                "required": True,
                "type": "string",
            },
            {
                "name": "tags",
                "in": "formData",
                "required": True,
                "type": "array",
                "items": {"type": "string"},
                "collectionFormat": "multi",
            },
            {"name": "title", "in": "formData", "required": True, "type": "string"},
            {
                "name": "description",
                "in": "formData",
                "required": True,
                "type": "string",
            },
            {
                "name": "embedded_link",
                "in": "formData",
                "required": True,
                "type": "string",
            },
            {
                "name": "platform",
                "in": "formData",
                "required": True,
                "type": "string",
                "enum": [e.value for e in GamePlatform],
            },
            {
                "name": "thumbnail",
                "in": "formData",
                "required": True,
                "type": "file",
            },
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
def create_game():
    converted_form = {
        "publisher_id": request.form.get("publisher_id"),
        "tags": request.form.getlist("tags"),
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "embedded_link": request.form.get("embedded_link"),
        "platform": request.form.get("platform"),
        "thumbnail": request.files["thumbnail"],
    }
    data = GameInputDTO().load(converted_form)
    try:
        game = g.game_service.create_game(data)
        mapped = GameOutputDTO().dump(game)
        return mapped
    except Exception as e:
        return {"errors": str(e)}, 400
