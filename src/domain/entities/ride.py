from datetime import datetime
from uuid import uuid4

from src.domain.constants import RideStatusEnum
from src.domain.models import Ride

from ._base_entitie import BaseEntitie


class RideEntitie(BaseEntitie):
    def __init__(
        self,
        passenger_id: str,
        ride_id: str = str(uuid4()),
        status: str = RideStatusEnum.CREATED.value,
        driver_id: str = None,
        rate: int = -1,
        fare: float = None,
        distance: float = None,
        from_latitude: float = None,
        from_longitude: float = None,
        to_latitude: float = None,
        to_longitude: float = None,
        created_at: str = datetime.now().isoformat(),
        updated_at: str = None,
    ):
        self._value = Ride(
            ride_id=ride_id,
            passenger_id=passenger_id,
            driver_id=driver_id,
            status=status,
            rate=rate,
            fare=fare,
            distance=distance,
            from_latitude=from_latitude,
            from_longitude=from_longitude,
            to_latitude=to_latitude,
            to_longitude=to_longitude,
            created_at=created_at,
            updated_at=updated_at,
        )

    def object(self, response: bool = False) -> Ride:
        result = super().object()
        if response:
            result.status = RideStatusEnum.create_from_value(result.status).name
        return result
