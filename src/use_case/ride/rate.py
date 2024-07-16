from src.domain.constants import RideStatusEnum
from src.domain.repositories import RideRepository
from src.presenter import ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import BaseUseCase


class RideRate(BaseUseCase):
    def __init__(self, ride_repository: RideRepository):
        super().__init__()
        self._ride_repository = ride_repository
        self.status = RideStatusEnum.FINISHED.value

    def run(self, ride_id: str, rate: int):
        self._validate_id(ride_id)
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if not ride.validate_next_state(new_status=self.status):
            raise ErrorStatusNotAllowed()
        return self._ride_repository.update_rate_repository(ride=ride, rate=rate, new_status=self.status)
