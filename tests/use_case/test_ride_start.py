from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import AccountEntitie, RideEntitie
from src.domain.models import Account, Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorRideOfOtherDriver,
    ErrorRideNotFound,
    ErrorStatusNotAllowed,
)
from src.use_case import RideStart
from tests.repositories import AccountTestRepository, RideTestRepository


@pytest.fixture
def account_repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


@pytest.fixture
def ride_repository() -> RideTestRepository:
    return RideTestRepository(db=None)


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
def ride_accept_other_driver(create_ride, ride_repository):
    ride_accept_other_driver = Ride(**create_ride.dict())
    ride_accept_other_driver.ride_id = str(uuid4())
    ride_accept_other_driver.driver_id = str(uuid4())
    ride_accept_other_driver.status = RideStatusEnum.ACCEPT.value
    return ride_repository.insert_ride(ride=ride_accept_other_driver)


@pytest.fixture
def ride_accept(create_ride, ride_repository):
    ride_accept = Ride(**create_ride.dict())
    ride_accept.ride_id = str(uuid4())
    ride_accept.status = RideStatusEnum.ACCEPT.value
    return ride_repository.insert_ride(ride=ride_accept)


@pytest.fixture
def ride_canceled(create_ride, ride_repository):
    ride_status_not_allowed = Ride(**create_ride.dict())
    ride_status_not_allowed.ride_id = str(uuid4())
    ride_status_not_allowed.status = RideStatusEnum.CANCELED.value
    return ride_repository.insert_ride(ride=ride_status_not_allowed)


def test_accept_ride_uuid_invalid(ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id="invalid_uuid", ride_id="invalid_uuid")


def test_accept_ride_not_found(ride_repository, account_driver):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=str(uuid4()))


def test_accept_ride_is_not_driver(ride_repository, account_passenger, ride_accept_other_driver):
    with pytest.raises(ErrorRideOfOtherDriver):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_passenger.account_id, ride_id=ride_accept_other_driver.ride_id)


def test_accept_ride_status_not_alowed(ride_repository, account_driver, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_canceled.ride_id)


def test_start_ride_success(ride_repository, account_driver, ride_accept):
    use_case = RideStart(ride_repository=ride_repository)
    ride = use_case.run(driver_id=account_driver.account_id, ride_id=ride_accept.ride_id)
    assert ride.driver_id == account_driver.account_id
    assert ride.status == RideStatusEnum.IN_PROGRESS.name
