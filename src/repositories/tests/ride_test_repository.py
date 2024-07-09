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

    def get_rides_by_driver(self, driver_id: str, status_in: RideStatusEnum, limit: int = 1) -> list[Ride]:
        result = []
        for ride in self.rides:
            if ride.driver_id == driver_id and ride.status in status_in:
                result.append(ride)
                if len(result) == limit:
                    return result
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
        return self.get_ride_by_id(id=ride.ride_id, response=True)

    def get_ride_by_id(self, id: str, response: bool = False):
        for item in self.rides:
            if item.ride_id == id:
                if response:
                    item.status = RideStatusEnum.create_from_value(item.status).name
                return item

    def update_driver_ride(self, ride: Ride, id_driver: int):
        for item in self.rides:
            if item.ride_id == ride.ride_id:
                item.driver_id = id_driver
                return item
