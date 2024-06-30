import abc

from domain.constants import RideStatusEnum

from ..models.ride import Ride
from src.database import Database


class RideRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db: Database) -> None:
        ...

    @abc.abstractmethod
    def insert_ride(self, ride: Ride) -> Ride:
        ...

    @abc.abstractmethod
    def get_rides_by_driver(self, driver_id: str, status: RideStatusEnum, limit: int) -> list[Ride]:
        ...

    @abc.abstractmethod
    def get_rides_by_passenger(self, passenger_id: str, status_not_in: list[RideStatusEnum], limit: int) -> list[Ride]:
        ...

    @abc.abstractmethod
    def update_status_ride(self, ride: Ride, new_status: RideStatusEnum):
        ...
