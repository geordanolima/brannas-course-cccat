from src.domain.constants import RideStatusEnum
from src.domain.repositories import RideRepository
from src.presenter import ErrorMissingInformation, ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import BaseUseCase


class RidePayment(BaseUseCase):
    def __init__(self, ride_repository: RideRepository) -> None:
        super().__init__()
        self._ride_repository = ride_repository
        self.status = RideStatusEnum.PENDING_RATE.value

    def run(self, ride_id: str, credit_card_token: str, amount: str):
        self._validate_id(ride_id)
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if not ride.validate_next_state(new_status=self.status):
            raise ErrorStatusNotAllowed()
        if not credit_card_token and not amount:
            raise ErrorMissingInformation()
        return self._ride_repository.update_status_ride(ride=ride, new_status=self.status)
