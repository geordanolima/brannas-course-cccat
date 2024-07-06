from ..domain.entities.coordinate import CoordinateEntitie
from ..provider import DatabaseProvider
from ..presenter.base_presenter import BasePresenter
from ..repositories import AccountDatabaseRepository, RideDatabaseRepository
from ..use_case.request_ride import RequestRide


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter().exception_handler
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)
        self.use_case = RequestRide(passenger_repository=self._account_repository, ride_repository=self._ride_repository)

    def create_ride(self, account: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        return self._presenter(method=self.use_case.create_new_route, params={account, from_coordinate, to_coordinate})
