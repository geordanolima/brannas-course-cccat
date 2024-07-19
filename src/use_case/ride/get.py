from src.presenter import ErrorIsInvalidUUID
from src.domain.models.ride import Ride
from src.domain.repositories import RideRepository
from src.use_case import BaseGetUseCase


class RideGet(BaseGetUseCase):
    def __init__(self, ride_repository: RideRepository) -> None:
        self._ride_repository = ride_repository

    def get_id(self, id: str) -> Ride:
        super().get_id(id=id)
        ride = self._ride_repository.get_ride_by_id(id=id, response=True)
        if not ride:
            raise ErrorIsInvalidUUID()
        return ride
