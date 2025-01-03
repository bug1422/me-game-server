from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.dtos.game import GameInputDTO,GameChangeLogInputDTO
from app.models.game import Game, GameChangeLog
from app.models.comment import Comment
from typing import List
from bson import ObjectId
from datetime import datetime
from app.dtos.comment import CommentInputDto
from app.tools.response import Response
from app.tools.wrapper.handle_response import handle_response


class GameService:
    def __init__(self, game_repo: GameRepository, user_repo: UserRepository):
        self.game_repo = game_repo
        self.user_repo = user_repo

    @handle_response
    def get_game_by_page(
        self,
        cur_page: int,
        page_size: int,
        tags: List[str] | None,
        game_engine: str,
        created_date: datetime | None,
    ):
        game_list, current_page, max_page = self.game_repo.get_by_filter(
            cur_page, page_size, tags, game_engine, created_date
        )
        return Response.success(
            response={
                "game_list": game_list,
                "current_page": current_page,
                "max_page": max_page,
            }
        )

    @handle_response
    def get_games(self):
        res = self.game_repo.get_all()
        return Response.success(response=res)

    @handle_response
    def get_game_by_id(self, id):
        games = self.game_repo.get_by_id(id)
        return Response.success(response=games)

    @handle_response
    def create_game(self, game_input: GameInputDTO) -> Game:
        user = self.user_repo.get_by_id(game_input["publisher_id"])
        if not user:
            raise Exception("User not found")
        game = Game(
            title=game_input["title"],
            tags=game_input["tags"],
            description=game_input["description"],
            embedded_link=game_input["embedded_link"],
            platform=game_input["platform"],
            publisher=user,
            game_engine=game_input["game_engine"].capitalize(),
            thumbnail=game_input["thumbnail"],
            game_content=game_input["game_content"],
        )
        game.save()
        return Response.success("Created successfully", game)

    @handle_response
    def add_comment(self, game_id, user_id, comment_input: CommentInputDto):
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise Exception("Game not found")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        if len(game.comments.filter(user_id=user_id)) > 1:
            raise Exception("You have reached limit")
        comment = Comment(content=comment_input["content"], user_id=user_id)
        parent_comment_id = comment_input.get('parent_id',None)
        print(parent_comment_id)
        if parent_comment_id:
            parent_coment = game.comments.filter(id=parent_comment_id)
            if not parent_coment:
                raise Exception("Parent comment not found")
            comment.parent_id = parent_comment_id
            comment.sub_thread_count = parent_coment.sub_thread_count + 1
        game.comments.append(comment)
        game.save()
        return Response.success("Added successfully", game)

    @handle_response
    def add_log(self, game_id: str, game_log: GameChangeLogInputDTO):
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise Exception("Game not found")
        major, minor, patch = map(int, game_log['version'].split("."))
        game.add_change_log(major,minor,patch,game_log['log'])
        return game

    @handle_response
    def delete_comment(self, game_id, user_id, comment_id):
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise Exception("Game not found")
        comment = game.comments.filter(id=comment_id).first()
        if not comment:
            raise Exception("Comment not found")
        elif comment.user_id != ObjectId(user_id):
            raise Exception("Not owner")
        game.comments = [
            comment for comment in game.comments if comment.id != ObjectId(comment_id)
        ]
        game.save()
        return Response.success("Removed successfully")

    # region Game Vote
    def _upvote(self, game, user):
        game.update(
            inc__upvote=1,
            add_to_set__upvote_list={
                "user_id": user.id,
                "user_nickname": user.nickname,
            },
        )

    def _remove_upvote(self, game, user):
        filtered_upvote_list = [
            voter for voter in game.upvote_list if voter.user_id != user.id
        ]
        game.update(
            __raw__={"$inc": {"upvote": -1}},
            set__upvote_list=filtered_upvote_list,
        )

    def _downvote(self, game, user):
        game.update(
            inc__downvote=1,
            add_to_set__downvote_list={
                "user_id": user.id,
                "user_nickname": user.nickname,
            },
        )

    def _remove_downvote(self, game, user):
        filtered_downvote_list = [
            voter for voter in game.downvote_list if voter.user_id != user.id
        ]
        game.update(
            __raw__={"$inc": {"downvote": -1}},
            set__downvote_list=filtered_downvote_list,
        )

    @handle_response
    def upvote_game(self, game_id, user_id):
        game = self.game_repo.get_by_id(game_id)
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        if not game:
            raise Exception("Game not found")
        if game.upvote_list.filter(user_id=user_id):
            self._remove_upvote(game, user)
        else:
            if game.downvote_list.filter(user_id=user_id):
                self._remove_downvote(game, user)
            self._upvote(game, user)
        game = self.game_repo.get_by_id(game_id)
        return Response.success("Action completed", game)

    @handle_response
    def downvote_game(self, game_id, user_id):
        game = self.game_repo.get_by_id(game_id)
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        if not game:
            raise Exception("Game not found")
        if game.downvote_list.filter(user_id=user_id):
            self._remove_downvote(game, user)
        else:
            if game.upvote_list.filter(user_id=user_id):
                self._remove_upvote(game, user)
            self._downvote(game, user)
        game = self.game_repo.get_by_id(game_id)
        return Response.success("Action completed", game)

    # endregion

    # region Comment Vote
    def _upvote_comment(self, comment, user):
        comment.upvote += 1
        comment.upvote_list.append(
            {
                "user_id": user.id,
                "user_nickname": user.nickname,
            }
        )

    def _downvote_comment(self, comment, user):
        comment.downvote += 1
        comment.downvote_list.append(
            {
                "user_id": user.id,
                "user_nickname": user.nickname,
            }
        )

    def _remove_upvote_comment(self, comment, user):
        comment.upvote -= 1
        voter_list = [
            voter for voter in comment.upvote_list if voter.user_id != user.id
        ]
        comment.upvote_list = voter_list

    def _remove_downvote_comment(self, comment, user):
        comment.downvote -= 1
        voter_list = [
            voter for voter in comment.downvote_list if voter.user_id != user.id
        ]
        comment.downvote_list = voter_list

    @handle_response
    def upvote_game_comment(self, game_id, user_id, comment_id):
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise Exception("Game not found")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        comment = game.comments.filter(id=ObjectId(comment_id)).first()
        if not comment:
            raise Exception("Comment not found")
        if comment.downvote_list.filter(user_id=user_id):
            self._remove_downvote_comment(comment, user)
        self._upvote_comment(comment, user)
        game.save()
        return Response.success("Upvote successfully", game)

    @handle_response
    def downvote_game_comment(self, game_id, user_id, comment_id):
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise Exception("Game not found")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        comment = game.comments.filter(id=ObjectId(comment_id)).first()
        if not comment:
            raise Exception("Comment not found")
        if comment.upvote_list.filter(user_id=user_id):
            self._remove_upvote_comment(comment, user)
        self._downvote_comment(comment, user)
        game.save()
        return Response.success("Downvote successfully", game)

    # endregion

    @handle_response
    def delete_game(self, id) -> bool:
        game = self.game_repo.get_by_id(id)
        if not game:
            raise Exception("Game not found")
        if game.thumbnail:
            game.thumbnail.delete()
            game.save()
        if game.game_content:
            game.game_content.delete()
            game.save()
        self.game_repo.delete(game)
        return Response.success("Delete successful")
