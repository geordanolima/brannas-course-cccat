from src.domain.value_objects import CoordinateObject
from src.provider import DatabaseProvider
from src.presenter.base_presenter import BasePresenter
from src.repositories import AccountDatabaseRepository, RideDatabaseRepository, PositionDatabaseRepository
from src.use_case import RideAccept, RideCreate, RideFinish, RideGet, RideStart, RideUpdatePosition


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter()
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)
        self._position_repository = PositionDatabaseRepository(db=self._database.connection)

    def create_ride(self, account: str, from_coordinate: CoordinateObject, to_coordinate: CoordinateObject):
        use_case = RideCreate(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[account, from_coordinate, to_coordinate])

    def accept_ride(self, ride_id: str, driver_id: str):
        use_case = RideAccept(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[driver_id, ride_id])

    def start_ride(self, ride_id: str, driver_id: str):
        use_case = RideStart(ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[driver_id, ride_id])

    def update_position(self, ride_id: str, coordinate: CoordinateObject):
        use_case = RideUpdatePosition(
            ride_repository=self._ride_repository, position_repository=self._position_repository
        )
        return self._presenter.exception_handler(method=use_case.run, params=[ride_id, coordinate])

    def finish_ride(self, ride_id: str):
        use_case = RideFinish(ride_repository=self._ride_repository, position_repository=self._position_repository)
        return self._presenter.exception_handler(method=use_case.run, params=[ride_id])

    def get_ride(self, id: str):
        use_case = RideGet(ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.get_id, params=[id])
