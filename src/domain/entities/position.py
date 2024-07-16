from datetime import datetime

from src.domain.models import Coordinate, Position

from ._base_entitie import BaseEntitie


class PositionEntitie(BaseEntitie):
    def __init__(
        self, position_id: str, ride_id: str, coordinate: Coordinate, created_at: str = datetime.now().isoformat()
    ):
        self._value = Position(
            position_id=position_id,
            ride_id=ride_id,
            latitude=coordinate.latitude,
            longitude=coordinate.longitude,
            created_at=created_at
        )
