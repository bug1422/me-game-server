from app.repositories.base_repository import BaseRepository
from app.models.game import Game
from typing import List
from mongoengine import Q
from datetime import datetime
from math import ceil


class GameRepository(BaseRepository[Game]):
    def __init__(self):
        super().__init__(Game)

    def get_by_filter(
        self,
        current_page: int,
        page_size: int,
        tags: List[str] | None,
        game_engine: str,
        created_date: datetime | None,
    ):
        filter = Q()
        if not current_page:
            current_page = 0
        if not page_size:
            page_size = 10
        if tags:
            filter &= Q(tags__in=[tag for tag in tags])
        if game_engine:
            filter &= Q(game_engine=game_engine)
        if created_date:
            filter &= Q(created_at=created_date)
        model_query = self.model.objects(filter)
        return (
            model_query.skip(current_page * page_size).limit(page_size),
            current_page,
            max(ceil(model_query.count() / page_size) - 1, 0),
        )
