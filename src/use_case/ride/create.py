from uuid import uuid4

from src.domain.constants import RideStatusEnum
from src.domain.entities import RideEntitie
from src.domain.models.ride import Ride
from src.domain.repositories import AccountRepository, RideRepository
from src.domain.value_objects import CoordinateObject
from src.presenter.errors import (
    ErrorAccountNotFound,
    ErrorCoordinatesEquals,
    ErrorHaveRideInProgress,
    ErrorIsNeedPassenger,
)
from src.use_case import BaseUseCase


class RideCreate(BaseUseCase):
    def __init__(self, ride_repository: RideRepository, passenger_repository: AccountRepository) -> None:
        super().__init__()
        self._account_repository = passenger_repository
        self._ride_repository = ride_repository

    def run(
        self, account_id: str, from_coordinate: CoordinateObject, to_coordinate: CoordinateObject
    ) -> Ride:
        self._validate_id(id=account_id)
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
        return self._ride_repository.insert_ride(ride=ride)
