from ..domain.entities.coordinate import CoordinateEntitie
from ..provider import DatabaseProvider
from ..presenter.base_presenter import BasePresenter
from ..repositories import AccountDatabaseRepository, RideDatabaseRepository
from ..use_case.ride_create import UCRide


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter()
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)

    def create_ride(self, account: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        try:
            use_case = UCRide(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
            ride = use_case.run(
                account_id=account,
                from_coordinate=from_coordinate,
                to_coordinate=to_coordinate
            )
            result = ride.dict()
            del result["MACHINE_STATUS"]
            return self._presenter.response(result)
        except BaseException as error:
            return self._presenter.response_error(error)
