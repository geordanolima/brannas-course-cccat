from ...database import Database
from ...domain.constants import RideStatusEnum
from ...domain.repositories import RideRepository
from ...domain.models import Ride


class RideTestRepository(RideRepository):
    def __init__(self, db: Database) -> None:
        self._db = db
        self.rides: list[Ride] = []

    def insert_ride(self, ride: Ride) -> Ride:
        self.rides.append(ride)
        return ride

    def get_rides_by_driver(self, driver_id: str, status: RideStatusEnum, limit: int) -> list[Ride]:
        result = []
        for ride in self.rides:
            if ride.driver_id == driver_id and ride.status == status:
                result.append(ride)
        return result

    def get_rides_by_passenger(self, passenger_id: str, status_not_in: list[int], limit: int) -> list[Ride]:
        result = []
        for ride in self.rides:
            if ride.passenger_id == passenger_id and ride.status not in status_not_in:
                result.append(ride)
        return result[:limit]

    def update_status_ride(self, ride: Ride, new_status: RideStatusEnum):
        for item in self.rides:
            if item.ride_id == ride.ride_id:
                item.status = new_status
