from src.database import Database
from src.domain.models.position import Position
from src.domain.repositories import PositionRepository


class PositionTestRepository(PositionRepository):
    def __init__(self, db: Database = None) -> None:
        self.db = db
        self.positions: list[Position] = []

    def insert_position(self, position: Position):
        self.positions.append(position)
        return self.get_position_by_id(position_id=position.position_id)

    def get_position_by_id(self, position_id: str) -> Position:
        for position in self.positions:
            if position.position_id == position_id:
                return position
        return None

    def get_position_by_ride(self, ride_id: str) -> list[Position]:
        result = []
        for position in self.positions:
            if position.ride_id == ride_id:
                result.append(position)
        return result
