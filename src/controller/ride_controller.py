from ..domain.entities.coordinate import CoordinateEntitie
from ..provider import DatabaseProvider
from ..presenter.base_presenter import BasePresenter
from ..repositories import AccountDatabaseRepository, RideDatabaseRepository
from ..use_case import RideAccept, RideCreate, RideGet


class RideController:
    def __init__(self) -> None:
        self._database = DatabaseProvider()
        self._presenter = BasePresenter()
        self._account_repository = AccountDatabaseRepository(db=self._database.connection)
        self._ride_repository = RideDatabaseRepository(db=self._database.connection)

    def create_ride(self, account: str, from_coordinate: CoordinateEntitie, to_coordinate: CoordinateEntitie):
        try:
            use_case = RideCreate(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
            ride = use_case.run(
                account_id=account,
                from_coordinate=from_coordinate,
                to_coordinate=to_coordinate
            )
            return self._presenter.response(ride.dict())
        except BaseException as error:
            return self._presenter.response_error(error)

    def accept_ride(self, ride_id: str, driver_id: str):
        try:
            use_case = RideAccept(passenger_repository=self._account_repository, ride_repository=self._ride_repository)
            ride = use_case.run(driver_id=driver_id, ride_id=ride_id)
            return self._presenter.response(ride.dict())
        except BaseException as error:
            return self._presenter.response_error(error)

    def get_ride(self, ride_id: str):
        use_case = RideGet(ride_repository=self._ride_repository)
        return self._presenter.exception_handler(method=use_case.run, params={ride_id})
