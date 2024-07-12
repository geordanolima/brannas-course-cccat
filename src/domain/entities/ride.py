from datetime import datetime

from src.domain.constants import RideStatusEnum
from src.domain.models import Ride

from ._base_entitie import BaseEntitie


class RideEntitie(BaseEntitie):
    def __init__(
        self,
        ride_id: str,
        passenger_id: str,
        status: str = RideStatusEnum.CREATED.value,
        driver_id: str = None,
        fare: float = None,
        distance: float = None,
        from_latitude: float = None,
        from_longitude: float = None,
        to_latitude: float = None,
        to_longitude: float = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = None,
    ):
        self._value = Ride(
            ride_id=ride_id,
            passenger_id=passenger_id,
            driver_id=driver_id,
            status=status,
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
        _value = super().object()
        if response:
            _value.status = RideStatusEnum.create_from_value(_value.status).name
        return _value
