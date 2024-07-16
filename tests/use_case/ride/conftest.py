from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import AccountEntitie, RideEntitie
from src.domain.models import Account, Ride
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
        rate=-1,
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
def ride_created(create_ride, ride_repository):
    ride_created = Ride(**create_ride.dict())
    ride_created.ride_id = str(uuid4())
    ride_created.driver_id = ""
    return ride_repository.insert_ride(ride=ride_created)


@pytest.fixture
def ride_in_progress(ride_repository, create_ride, account_driver) -> Ride:
    create_ride.status = RideStatusEnum.IN_PROGRESS.value
    create_ride.driver_id = account_driver.account_id
    ride_repository.insert_ride(create_ride)
    return create_ride

@pytest.fixture
def ride_pending_pay(ride_repository, create_ride, account_driver) -> Ride:
    create_ride.status = RideStatusEnum.PENDING_PAY.value
    create_ride.driver_id = account_driver.account_id
    ride_repository.insert_ride(create_ride)
    return create_ride

@pytest.fixture
def ride_pending_rate(ride_repository, create_ride, account_driver) -> Ride:
    create_ride.status = RideStatusEnum.PENDING_RATE.value
    create_ride.driver_id = account_driver.account_id
    ride_repository.insert_ride(create_ride)
    return create_ride


@pytest.fixture
def ride_canceled(create_ride, ride_repository):
    ride_status_not_allowed = Ride(**create_ride.dict())
    ride_status_not_allowed.ride_id = str(uuid4())
    ride_status_not_allowed.driver_id = ""
    ride_status_not_allowed.status = RideStatusEnum.CANCELED.value
    return ride_repository.insert_ride(ride=ride_status_not_allowed)
