from ..domain.entities.coordinate import CoordinateEntitie
from ..provider import DatabaseProvider
from ..presenter.base_presenter import BasePresenter
from ..repositories import AccountDatabaseRepository, RideDatabaseRepository
from ..use_case.route import Route


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter()
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)

    def run(self, account: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        use_case = Route(passenger_repository=self._account_repository, _ride_repository=self._ride_repository)
        return use_case.create_new_route(
            account_id=account,
            from_coordinate=from_coordinate,
            to_coordinate=to_coordinate
        )
