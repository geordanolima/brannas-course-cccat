from src.domain.constants import RideStatusEnum
from src.domain.repositories import RideRepository
from src.presenter import (
    ErrorRideNotFound,
    ErrorRideOfOtherDriver,
    ErrorStatusNotAllowed,
)
from src.use_case import BaseUseCase


class RideStart(BaseUseCase):
    def __init__(self, ride_repository: RideRepository) -> None:
        super().__init__()
        self._ride_repository = ride_repository
        self.staus = RideStatusEnum.IN_PROGRESS.value

    def run(self, driver_id: str, ride_id: str):
        self._validate_list_id(list_id=[driver_id, ride_id])
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if ride.driver_id != driver_id:
            raise ErrorRideOfOtherDriver()
        if not ride.validate_next_state(new_status=self.staus):
            raise ErrorStatusNotAllowed()
        return self._ride_repository.update_status_ride(ride=ride, new_status=self.staus)
