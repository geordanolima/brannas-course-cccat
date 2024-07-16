from datetime import datetime

from src.database import Database
from src.domain.constants import RideStatusEnum
from src.domain.repositories import RideRepository
from src.domain.models import Ride


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
                item.updated_at = datetime.now()
        return self.get_ride_by_id(id=ride.ride_id, response=True)

    def get_ride_by_id(self, id: str, response: bool = False):
        for item in self.rides:
            if item.ride_id == id:
                if response:
                    item.status = RideStatusEnum.create_from_value(item.status).name
                return item

    def update_driver_ride(self, ride: Ride, id_driver: int, new_status: int):
        for item in self.rides:
            if item.ride_id == ride.ride_id:
                item.driver_id = id_driver
                item.status = new_status
                item.updated_at = datetime.now()
                return item

    def update_fare_ride(self, ride: Ride, fare: float, distance: float, new_status) -> Ride:
        for item in self.rides:
            if item.ride_id == ride.ride_id:
                item.fare = fare
                item.distance = distance
                item.status = new_status
                item.updated_at = datetime.now()
                return item

    def update_rate_repository(self, ride: Ride, rate: int, new_status: int) -> Ride:
        for item in self.rides:
            if item.ride_id == ride.ride_id:
                item.rate = rate
                item.status = new_status
                item.updated_at = datetime.now()
                return item
