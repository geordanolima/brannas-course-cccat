from ..domain.models.ride import Ride
from ..domain.repositories import RideRepository


class RideGet:
    def __init__(self, ride_repository: RideRepository) -> None:
        self._ride_repository = ride_repository

    def run(self, ride_id: str) -> Ride:
        return self._ride_repository.get_ride_by_id(id=ride_id)
