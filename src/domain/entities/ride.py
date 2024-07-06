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
        from_latitude: float = None,
        from_longitude: float = None,
        to_latitude: float = None,
        to_longitude: float = None,
        date: datetime = datetime.now(),
    ):
        self._ride = Ride(
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
            date=date,
        )

    def object(self) -> Ride:
        self._ride.date = self._ride.date.isoformat()
        return self._ride
