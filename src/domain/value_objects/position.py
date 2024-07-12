from datetime import datetime

from src.domain.models import Coordinate, Position


class PositionObject:
    def __init__(self, position_id: str, ride_id: str, coordinate: Coordinate, created_at: datetime = datetime.now()):
        self._position = Position(
            position_id=position_id,
            ride_id=ride_id,
            latitude=coordinate.latitude,
            longitude=coordinate.longitude,
            created_at=created_at
        )

    def object(self) -> Position:
        if type(self._position.created_at) is datetime:
            self._position.created_at = self._position.created_at.isoformat()
        return self._position
