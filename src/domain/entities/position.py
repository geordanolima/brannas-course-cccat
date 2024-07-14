from datetime import datetime

from ._base_entitie import BaseEntitie
from src.domain.models import Coordinate, Position

class PositionEntitie(BaseEntitie):
    def __init__(self, position_id: str, ride_id: str, coordinate: Coordinate, created_at: datetime = datetime.now()):
        self._value = Position(
            position_id=position_id,
            ride_id=ride_id,
            latitude=coordinate.latitude,
            longitude=coordinate.longitude,
            created_at=created_at
        )
