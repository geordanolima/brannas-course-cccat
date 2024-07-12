from src.presenter import ErrorIsInvalidUUID
from src.domain.models.ride import Ride
from src.domain.repositories import RideRepository


class RideGet:
    def __init__(self, ride_repository: RideRepository) -> None:
        self._ride_repository = ride_repository

    def run(self, ride_id: str) -> Ride:
        if not self._validate.is_uuid(id=ride_id):
            raise ErrorIsInvalidUUID()
        ride = self._ride_repository.get_ride_by_id(id=ride_id, response=True)
        if not ride:
            raise ErrorIsInvalidUUID()
        return ride
