from uuid import uuid4

from ..domain.constants import RideStatusEnum
from ..domain.entities import CoordinateEntitie, RideEntitie
from ..domain.repositories import AccountRepository, RideRepository
from ..utils.errors import ErrorIsNeedPassenger, ErrorHaveRideInProgress


class Route:
    def __init__(self, ride_repository: RideRepository, passenger_repository: AccountRepository) -> None:
        self._account_repository = passenger_repository
        self._ride_repository = ride_repository

    def create_new_route(self, account_id: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        account = self._account_repository.get_account_by_id(id=account_id)
        if not account.is_passenger:
            raise ErrorIsNeedPassenger()
        if self._ride_repository.get_rides_by_passenger(
            passenger_id=account.account_id,
            status_not_in=[RideStatusEnum.FINISHED, RideStatusEnum.CANCELED, RideStatusEnum.ERROR],
        ):
            raise ErrorHaveRideInProgress()
        ride = RideEntitie(
            id=uuid4(),
            from_lat=from_coordinate.latitude,
            from_long=from_coordinate.longitude,
            to_lat=to_coordinate.latitude,
            to_long=to_coordinate.longitude
        )
        return self._ride_repository.insert_ride(ride=ride)
