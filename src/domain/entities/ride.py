from datetime import datetime

from ..models.ride import Ride


class RideEntitie(Ride):
    def __init__(
        self,
        ride_id: str,
        passenger_id: str,
        driver_id: str,
        status: str,
        fare: float = None,
        distance: float = None,
        from_lat: float = None,
        from_long: float = None,
        to_lat: float = None,
        to_long: float = None,
        date: datetime = datetime.now(),
    ):
        self.ride = Ride(
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
        return self.ride
