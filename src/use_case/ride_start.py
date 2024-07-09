from ..domain.constants import RideStatusEnum
from ..domain.repositories import RideRepository
from ..presenter import (
    ErrorIsInvalidUUID,
    ErrorRideNotFound,
    ErrorRideOfOtherDriver,
    ErrorStatusNotAllowed,
)
from ..utils.validates import Validates


class RideStart:
    def __init__(self, ride_repository: RideRepository) -> None:
        self._ride_repository = ride_repository
        self._validate = Validates()
        self.staus = RideStatusEnum.IN_PROGRESS.value

    def run(self, driver_id: str, ride_id: str):
        if not self._validate.is_uuid(id=driver_id) or not self._validate.is_uuid(id=ride_id):
            raise ErrorIsInvalidUUID()
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if ride.driver_id != driver_id:
            raise ErrorRideOfOtherDriver()
        if not ride.validate_next_state(new_status=self.staus):
            raise ErrorStatusNotAllowed()
        return self._ride_repository.update_status_ride(ride=ride, new_status=self.staus)
