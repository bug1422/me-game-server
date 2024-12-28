from app.repositories.base_repository import BaseRepository
from app.models.game import Game


class GameRepository(BaseRepository[Game]):
    def __init__(self):
        super().__init__(Game)
