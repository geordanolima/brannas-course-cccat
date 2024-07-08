from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import AccountEntitie, RideEntitie
from src.domain.models import Account, Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorAccountNotFound,
    ErrorRideNotFound,
    ErrorIsNeedDriver,
    ErrorRideInProgress,
    ErrorHaveRideInProgress,
    ErrorStatusNotAllowed,
)
from src.repositories.tests import AccountTestRepository, RideTestRepository
from src.use_case import RideAccept


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
        password="12345",
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


@pytest.fixture
def ride_canceled(create_ride, ride_repository):
    ride_status_not_allowed = Ride(**create_ride.dict())
    ride_status_not_allowed.ride_id = str(uuid4())
    ride_status_not_allowed.driver_id = ""
    ride_status_not_allowed.status = RideStatusEnum.CANCELED.value
    return ride_repository.insert_ride(ride=ride_status_not_allowed)


def test_accept_ride_uuid_invalid(account_repository, ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id="invalid_uuid", ride_id="invalid_uuid")


def test_accept_ride_account_not_found(account_repository, ride_repository):
    with pytest.raises(ErrorAccountNotFound):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=str(uuid4()), ride_id=str(uuid4()))


def test_accept_ride_not_found(account_repository, ride_repository, account_driver):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=str(uuid4()))


def test_accept_ride_is_not_driver(account_repository, ride_repository, account_passenger):
    with pytest.raises(ErrorIsNeedDriver):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_passenger.account_id, ride_id=str(uuid4()))


def test_accept_driver_have_other_ride(
    account_repository, ride_repository, account_driver, ride_in_progress, ride_created
):
    with pytest.raises(ErrorHaveRideInProgress):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_created.ride_id)


def test_accept_ride_status_not_alowed(account_repository, ride_repository, account_driver, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_canceled.ride_id)



def test_accept_ride_success(account_repository, ride_repository, account_driver, ride_created):
    use_case = RideAccept(passenger_repository=account_repository, ride_repository=ride_repository)
    ride = use_case.run(driver_id=account_driver.account_id, ride_id=ride_created.ride_id)
    assert ride.driver_id == account_driver.account_id
    assert ride.status == RideStatusEnum.ACCEPT.value
