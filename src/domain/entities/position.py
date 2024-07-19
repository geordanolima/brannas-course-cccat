from datetime import datetime
from uuid import uuid4

from src.domain.models import Coordinate, Position

from ._base_entitie import BaseEntitie


class PositionEntitie(BaseEntitie):
    def __init__(
        self,
        ride_id: str,
        coordinate: Coordinate,
        position_id: str = str(uuid4()),
        created_at: str = datetime.now().isoformat()
    ):
        self._value = Position(
            position_id=position_id,
            ride_id=ride_id,
            latitude=coordinate.latitude,
            longitude=coordinate.longitude,
            created_at=created_at
        )
