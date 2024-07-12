import abc

from src.database import Database
from src.domain.models.position import Position


class PositionRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db: Database) -> None:
        ...

    @abc.abstractmethod
    def insert_position(self, position: Position):
        ...

    @abc.abstractmethod
    def get_position_by_id(self, position_id: str) -> Position:
        ...

    @abc.abstractmethod
    def get_position_by_ride(self, ride_id: str) -> list[Position]:
        ...
