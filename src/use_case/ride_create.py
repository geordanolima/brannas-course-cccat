from uuid import uuid4

from ..domain.constants import RideStatusEnum
from ..domain.entities import CoordinateEntitie, RideEntitie
from ..domain.models.ride import Ride
from ..domain.repositories import AccountRepository, RideRepository
from ..presenter.errors import (
    ErrorAccountNotFound,
    ErrorCoordinatesEquals,
    ErrorHaveRideInProgress,
    ErrorIsInvalidUUID,
    ErrorIsNeedPassenger,
)
from ..utils.validates import Validates


class RideCreate:
    def __init__(self, ride_repository: RideRepository, passenger_repository: AccountRepository) -> None:
        self._account_repository = passenger_repository
        self._ride_repository = ride_repository
        self._validate = Validates()

    def run(
        self, account_id: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie
    ) -> Ride:
        if not self._validate.is_uuid(id=account_id):
            raise ErrorIsInvalidUUID()
        account = self._account_repository.get_account_by_id(id=account_id)
        if not account:
            raise ErrorAccountNotFound()
        if not account.is_passenger:
            raise ErrorIsNeedPassenger()
        if self._ride_repository.get_rides_by_passenger(
            passenger_id=account.account_id,
            status_not_in=[RideStatusEnum.FINISHED.value, RideStatusEnum.CANCELED.value, RideStatusEnum.ERROR.value],
            limit=1
        ):
            raise ErrorHaveRideInProgress()
        if from_coordinate == to_coordinate:
            raise ErrorCoordinatesEquals()
        ride = RideEntitie(
            ride_id=str(uuid4()),
            passenger_id=account.account_id,
            from_latitude=from_coordinate.latitude,
            from_longitude=from_coordinate.longitude,
            to_latitude=to_coordinate.latitude,
            to_longitude=to_coordinate.longitude
        ).object()
        self._ride_repository.insert_ride(ride=ride)
        return self._ride_repository.get_ride_by_id(id=ride.ride_id)
