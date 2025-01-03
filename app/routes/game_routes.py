from flask import request, Blueprint, g
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity
from flasgger import swag_from
from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.services.game_service import GameService
from app.models.game import GamePlatform
from app.dtos.game import (
    GameInputDTO,
    GameDetailOutputDTO,
    GameThumbnailOutputDTO,
    GamePagingDTO,
    GameChangeLogInputDTO,
    GameChangeLogOutputDTO,
)
from app.dtos.comment import CommentInputDto
from app.tools.response import Response
from app.dtos.response import ResponseDTO

game_routes = Blueprint("game_routes", __name__)


@game_routes.before_request
def before_request():
    g.game_repo = GameRepository()
    g.user_repo = UserRepository()
    g.game_service = GameService(g.game_repo, g.user_repo)


@game_routes.get("/get-game-list")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {
                "name": "tags",
                "in": "query",
                "required": False,
                "type": "array",
                "items": {"type": "string"},
                "collectionFormat": "multi",
            },
            {
                "name": "game_engine",
                "in": "query",
                "required": False,
                "type": "string",
            },
            {
                "name": "current_page",
                "in": "query",
                "required": False,
                "type": "integer",
            },
            {
                "name": "page_size",
                "in": "query",
                "required": False,
                "type": "integer",
            },
        ],
        "responses": {
            "200": {"description": "get test"},
        },
    }
)
def get_games_by_page():
    res: Response = g.game_service.get_game_by_page(
        request.args.get("current_page"),
        request.args.get("page_size"),
        request.args.getlist("tags"),
        request.args.getlist("game_engine"),
        None,
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GamePagingDTO), 200


@game_routes.get("/detail/<game_id>")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {
                "name": "game_id",
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
def get_game_by_id(game_id):
    res: Response = g.game_service.get_game_by_id(game_id)
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 200


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
                "name": "game_engine",
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
            {
                "name": "game_content",
                "in": "formData",
                "required": False,
                "type": "file",
            },
        ],
        "responses": {
            "201": {
                "description": "User created successfully",
            },
            "400": {"description": "Invalid data"},
        },
    }
)
def create_game():
    print(request.files)
    converted_form = {
        "publisher_id": request.form.get("publisher_id"),
        "tags": request.form.getlist("tags"),
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "embedded_link": request.form.get("embedded_link"),
        "platform": request.form.get("platform"),
        "game_engine": request.form.get("game_engine"),
        "thumbnail": request.files.get("thumbnail"),
        "game_content": request.files.get("game_content"),
    }
    data = GameInputDTO().load(converted_form)
    res: Response = g.game_service.create_game(data)
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 201


@game_routes.post("/add-log")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {
                "name": "log",
                "in": "body",
                "description": "Game log data",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "game_id": {
                            "type": "string",
                            "required": True,
                        },
                        "version": {
                            "type": "string",
                            "required": True,
                        },
                        "log": {
                            "type": "string",
                            "required": False,
                        },
                    },
                },
                "example": {
                    "game_id": "1220981209123",
                    "version": "1.0.0",
                    "log": "default update",
                },
            }
        ],
        "responses": {
            "201": {
                "description": "Log created successfully",
            },
            "400": {"description": "Invalid data"},
        },
    }
)
@jwt_required()
def add_log():
    data = request.get_json()
    game_log = GameChangeLogInputDTO().dump(data)
    res: Response = g.game_service.add_log(data["game_id"], game_log)
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 201


@game_routes.post("/add-comment")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {
                "name": "comment",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "game_id": {"type": "string", "required": True},
                        "parent_id": {"type": "string", "required": False},
                        "content": {"type": "string", "required": True},
                    },
                },
            }
        ],
        "responses": {
            "201": {"description": "comment created"},
            "400": {"description": "Invalid data"},
        },
    }
)
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    game_json = request.get_json()
    comment_input = CommentInputDto().load(game_json)
    res: Response = g.game_service.add_comment(
        game_json["game_id"], user_id, comment_input
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 201


@game_routes.put("/upvote")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {"name": "game_id", "in": "query", "type": "string"},
            {"name": "user_id", "in": "query", "type": "string"},
        ],
        "responses": {"200": {"description": "Game upvoted"}},
    }
)
def upvote_game():
    res: Response = g.game_service.upvote_game(
        request.args.get("game_id"), request.args.get("user_id")
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 200


@game_routes.put("/downvote")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {"name": "game_id", "in": "query", "type": "string"},
            {"name": "user_id", "in": "query", "type": "string"},
        ],
        "responses": {"200": {"description": "Game downvoted"}},
    }
)
def downvote_game():
    res: Response = g.game_service.downvote_game(
        request.args.get("game_id"), request.args.get("user_id")
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 200


@game_routes.put("/upvote/comment")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {"name": "game_id", "in": "query", "type": "string"},
            {"name": "user_id", "in": "query", "type": "string"},
            {"name": "comment_id", "in": "query", "type": "string"},
        ],
        "responses": {"200": {"description": "Comment upvoted"}},
    }
)
def upvote_comment():
    res: Response = g.game_service.upvote_game_comment(
        request.args.get["game_id"],
        request.args.get["user_id"],
        request.args.get["comment_id"],
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 200


@game_routes.put("/downvote/comment")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [
            {"name": "game_id", "in": "query", "type": "string"},
            {"name": "user_id", "in": "query", "type": "string"},
            {"name": "comment_id", "in": "query", "type": "string"},
        ],
        "responses": {"200": {"description": "Comment downvoted"}},
    }
)
def downvote_comment():
    res: Response = g.game_service.downvote_game_comment(
        request.args.get["game_id"],
        request.args.get["user_id"],
        request.args.get["comment_id"],
    )
    if not res.result:
        return ResponseDTO.convert(res), 404
    return ResponseDTO.convert(res, GameDetailOutputDTO), 200


@game_routes.delete("/<game_id>")
@swag_from(
    {
        "tags": ["Games"],
        "parameters": [{"name": "game_id", "in": "path", "type": "string"}],
        "responses": {
            "200": {"description": "Game deleted"},
            "400": {"description": "Invalid data"},
        },
    }
)
def delete_game(game_id):
    res: Response = g.game_service.delete_game(game_id)
    if not res.result:
        return ResponseDTO.convert(res), 404
    else:
        return ResponseDTO.convert(res), 200
