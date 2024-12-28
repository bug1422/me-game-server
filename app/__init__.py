from flask import Flask, g
from flask_mongoengine import MongoEngine
from flasgger import Swagger
from app.routes.user_routes import user_routes
from app.routes.game_routes import game_routes
from app.repositories.user_repository import UserRepository


def create_app(config):
    db = MongoEngine()
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Swagger(app)
    app.register_blueprint(user_routes, url_prefix="/users")
    app.register_blueprint(game_routes, url_prefix="/games")

    @app.get("/")
    def homepage():
        return {"message": "connected to api"}

    return app
