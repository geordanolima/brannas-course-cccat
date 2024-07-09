from ..domain.entities.coordinate import CoordinateEntitie
from ..provider import DatabaseProvider
from ..presenter.base_presenter import BasePresenter
from ..repositories import AccountDatabaseRepository, RideDatabaseRepository
from ..use_case import RideAccept, RideCreate, RideGet, RideStart


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter()
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)

    def create_ride(self, account: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        use_case = RideCreate(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[account, from_coordinate, to_coordinate])

    def accept_ride(self, ride_id: str, driver_id: str):
        use_case = RideAccept(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[driver_id, ride_id])

    def start_ride(self, ride_id: str, driver_id: str):
        use_case = RideStart(ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[driver_id, ride_id])

    def get_ride(self, ride_id: str):
        use_case = RideGet(ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[ride_id])
