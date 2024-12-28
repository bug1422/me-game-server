from typing import Type, TypeVar, Generic, List
from mongoengine import Document
from bson import ObjectId

T = TypeVar("T", bound=Document)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self) -> List[T]:
        return self.model.objects

    def get_by_id(self, id: str) -> T:
        return self.model.objects(id=id).first()

    def add(self, entity: T) -> T:
        entity.save()
        return entity

    def update(self, entity: T) -> T:
        entity.update()
        return entity

    def delete(self, entity: T) -> None:
        entity.delete()
