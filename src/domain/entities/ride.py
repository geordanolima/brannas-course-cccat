from datetime import datetime

from ...domain.constants import RideStatusEnum

from ..models.ride import Ride


class RideEntitie:
    def __init__(
        self,
        ride_id: str,
        passenger_id: str,
        status: str = RideStatusEnum.CREATED.value,
        driver_id: str = None,
        fare: float = None,
        distance: float = None,
        from_lat: float = None,
        from_long: float = None,
        to_lat: float = None,
        to_long: float = None,
        date: datetime = datetime.now(),
    ):
        self._ride = Ride(
            ride_id=ride_id,
            passenger_id=passenger_id,
            driver_id=driver_id,
            status=status,
            fare=fare,
            distance=distance,
            from_lat=from_lat,
            from_long=from_long,
            to_lat=to_lat,
            to_long=to_long,
            date=date,
        )

    def object(self) -> Ride:
        return self._ride
