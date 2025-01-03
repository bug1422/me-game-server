from flask import Flask, g, request
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
)
from flask_bcrypt import Bcrypt
from flasgger import Swagger
from app.routes.user_routes import user_routes
from app.routes.game_routes import game_routes
from app.repositories.user_repository import UserRepository

template = {
    "swagger": "2.0",
    "info": {
        "title": "MeGame API",
        "description": "BUG1422 documentation.",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "paths": {},
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "\
                JWT Authorization header"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger_config = {
    "headers": [

        ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "specs_route": "/apidocs/",
    "swagger_ui": True,
    "swagger_ui_config": {
        "persistAuthorization": True,
        "authAction": {
            "Bearer": {
                "name": "Authorization",
                "schema": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Paste the token below. The Bearer prefix will be automatically added."
                },
            }
        },
    }
}

db = MongoEngine()
bcrypt = Bcrypt()
jwt = JWTManager()
swagger = Swagger(template=template,config=swagger_config)


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(user_routes, url_prefix="/users")
    app.register_blueprint(game_routes, url_prefix="/games")

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    @app.get("/")
    def homepage():
        return {"message": "connected to api"}

    return app
