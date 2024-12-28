from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.dtos.game import GameInputDTO
from app.models.game import Game


class GameService:
    def __init__(self, game_repo: GameRepository, user_repo: UserRepository):
        self.game_repo = game_repo
        self.user_repo = user_repo

    def get_games(self):
        res = self.game_repo.get_all()
        print(res)
        return res

    def get_game_by_id(self, id):
        return self.game_repo.get_by_id(id)

    def create_game(self, game_input: GameInputDTO) -> Game:
        user = self.user_repo.get_by_id(game_input["publisher_id"])
        if not user:
            return "Can't find publisher account"
        game = Game(
            title=game_input["title"],
            tags=game_input["tags"],
            description=game_input["description"],
            embedded_link=game_input["embedded_link"],
            platform=game_input["platform"],
            publisher=user,
            thumbnail=game_input["thumbnail"],
        )
        game.save()
        return game
