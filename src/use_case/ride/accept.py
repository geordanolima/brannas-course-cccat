from src.domain.constants import RideStatusEnum
from src.domain.repositories import AccountRepository, RideRepository
from src.presenter import (
    ErrorAccountNotFound,
    ErrorHaveRideInProgress,
    ErrorIsNeedDriver,
    ErrorRideNotFound,
    ErrorStatusNotAllowed,
)
from src.use_case import BaseUseCase


class RideAccept(BaseUseCase):
    def __init__(self, ride_repository: RideRepository, passenger_repository: AccountRepository) -> None:
        super().__init__()
        self._account_repository = passenger_repository
        self._ride_repository = ride_repository
        self.status = RideStatusEnum.ACCEPT.value

    def run(self, driver_id: str, ride_id: str):
        self._validate_list_id(list_id=[driver_id, ride_id])
        account = self._account_repository.get_account_by_id(id=driver_id)
        if not account:
            raise ErrorAccountNotFound()
        if not account.is_driver:
            raise ErrorIsNeedDriver()
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if not ride.validate_next_state(new_status=self.status):
            raise ErrorStatusNotAllowed()
        if self._ride_repository.get_rides_by_driver(driver_id=driver_id, status_in=[
            RideStatusEnum.ACCEPT.value,
            RideStatusEnum.IN_PROGRESS.value,
            RideStatusEnum.PENDING_PAY.value,
            RideStatusEnum.PENDING_RATE.value
        ], limit=1):
            raise ErrorHaveRideInProgress()
        return self._ride_repository.update_driver_ride(ride=ride, id_driver=driver_id, new_status=self.status)
