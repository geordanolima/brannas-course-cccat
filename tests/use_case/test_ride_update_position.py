from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import AccountEntitie, RideEntitie
from src.domain.models import Account, Coordinate, Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorRideNotFound,
    ErrorStatusNotAllowed,
)
from src.use_case import RideUpdatePosition
from tests.repositories import AccountTestRepository, RideTestRepository, PositionTestRepository


@pytest.fixture
def account_repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


@pytest.fixture
def ride_repository() -> RideTestRepository:
    return RideTestRepository(db=None)


@pytest.fixture
def position_repository() -> PositionTestRepository:
    return PositionTestRepository(db=None)


@pytest.fixture
def create_account() -> Account:
    return AccountEntitie(
        account_id=str(uuid4()),
        name="test name",
        email="test@test.com",
        password="Senha@segura123",
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
    ).object()


@pytest.fixture
def account_driver(create_account, account_repository) -> Account:
    account_driver = Account(**create_account.dict())
    account_driver.account_id = str(uuid4())
    account_driver.is_passenger = False
    account_driver.is_driver = True
    account_driver.car_plate = "XXX-1234"
    account_repository.insert_account(account=account_driver)
    return account_driver


@pytest.fixture
def account_passenger(create_account, account_repository) -> Account:
    account_passenger = Account(**create_account.dict())
    account_passenger.account_id = str(uuid4())
    account_passenger.is_driver = False
    account_passenger.is_passenger = True
    account_repository.insert_account(account=account_passenger)
    return account_passenger


@pytest.fixture
def create_ride(account_passenger, account_driver) -> Ride:
    return RideEntitie(
        ride_id=str(uuid4()),
        passenger_id=account_passenger.account_id,
        driver_id=account_driver.account_id,
        status=RideStatusEnum.CREATED.value,
    ).object()


@pytest.fixture
def ride_in_progress(create_ride, ride_repository):
    ride_in_progress = Ride(**create_ride.dict())
    ride_in_progress.ride_id = str(uuid4())
    ride_in_progress.status = RideStatusEnum.IN_PROGRESS.value
    return ride_repository.insert_ride(ride=ride_in_progress)


@pytest.fixture
def ride_created(create_ride, ride_repository):
    ride_created = Ride(**create_ride.dict())
    ride_created.ride_id = str(uuid4())
    ride_created.driver_id = ""
    return ride_repository.insert_ride(ride=ride_created)


def test_update_positon_uuid_invalid(ride_repository, position_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id="invalid_uuid", coordinate=Coordinate(latitude=10, longitude=11))


def test_update_position_ride_not_found(ride_repository, position_repository):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=str(uuid4()), coordinate=Coordinate(latitude=10, longitude=11))


def test_update_position_status_not_allwed(ride_repository, position_repository, ride_created):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=ride_created.ride_id, coordinate=Coordinate(latitude=10, longitude=11))


def test_success_update_position(ride_repository, position_repository, ride_in_progress):
    use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
    position = use_case.run(ride_id=ride_in_progress.ride_id, coordinate=Coordinate(latitude=10, longitude=11))
    assert position.position_id is not None
    assert position.latitude == 10
    assert position.longitude == 11
