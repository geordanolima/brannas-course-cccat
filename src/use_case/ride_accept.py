from ..domain.constants import RideStatusEnum
from ..domain.repositories import AccountRepository, RideRepository
from ..presenter.errors import (
    ErrorAccountNotFound,
    ErrorHaveRideInProgress,
    ErrorIsInvalidUUID,
    ErrorIsNeedDriver,
    ErrorRideInProgress,
    ErrorRideNotFound,
)
from ..utils.validates import Validates


class RideAccept:
    def __init__(self, ride_repository: RideRepository, passenger_repository: AccountRepository) -> None:
        self._account_repository = passenger_repository
        self._ride_repository = ride_repository
        self._validate = Validates()

    def run(self, driver_id: str, ride_id: str):
        if not self._validate.is_uuid(id=driver_id) or not self._validate.is_uuid(id=ride_id):
            raise ErrorIsInvalidUUID()
        account = self._account_repository.get_account_by_id(id=driver_id)
        if not account:
            raise ErrorAccountNotFound()
        if not account.is_driver:
            raise ErrorIsNeedDriver()
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if ride.status != RideStatusEnum.CREATED.value:
            raise ErrorRideInProgress()
        if self._ride_repository.get_rides_by_driver(driver_id=driver_id, status_in=[
            RideStatusEnum.ACCEPT.value,
            RideStatusEnum.IN_PROGRESS.value,
            RideStatusEnum.PENDING_PAY.value,
            RideStatusEnum.PENDING_RATE.value
        ]):
            raise ErrorHaveRideInProgress()
        # maquina de estado
        self._ride_repository.update_driver_ride(ride=ride, driver_id=driver_id)
        self._ride_repository.update_status_ride(ride=ride, new_status=RideStatusEnum.ACCEPT.value)
        return self._ride_repository.get_ride_by_id(id=ride_id)
