from uuid import uuid4
import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import AccountEntitie, CoordinateEntitie, RideEntitie
from src.domain.models import Account, Ride
from src.repositories.tests import AccountTestRepository, RideTestRepository
from src.use_case.route import Route
from src.utils.errors import ErrorHaveRideInProgress, ErrorIsNeedPassenger


account_repository = AccountTestRepository(db=None)
ride_repository = RideTestRepository(db=None)


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
def create_ride(account_passenger, account_driver) -> Ride:
    return RideEntitie(
        ride_id=str(uuid4),
        passenger_id=account_passenger.account_id,
        driver_id=account_driver.account_id,
        status=RideStatusEnum.CREATED.value,
    ).object()

@pytest.fixture
def account_not_passenger(create_account) -> Account:
    account = AccountEntitie(**create_account.dict())
    account.is_passenger = False
    account_repository.insert_account(account=account)
    return account


@pytest.fixture
def account_passenger(create_account) -> Account:
    account_passenger = AccountEntitie(**create_account.dict())
    account_passenger.account_id = str(uuid4())
    account_passenger.is_driver = False
    account_passenger.is_passenger = True
    account_repository.insert_account(account=account_passenger.object())
    return account_passenger.object()


@pytest.fixture
def account_driver(create_account) -> Account:
    account_driver = AccountEntitie(**create_account.dict())
    account_driver.account_id = str(uuid4())
    account_driver.is_passenger = False
    account_driver.is_driver = True
    account_driver.car_plate = "XXX-1234"
    account_repository.insert_account(account=account_driver.object)
    return account_driver.object()


@pytest.fixture
def ride_in_progress(create_ride, account_driver) -> Ride:
    create_ride.status = RideStatusEnum.IN_PROGRESS.value
    create_ride.driver_id = account_driver.account_id
    ride_repository.insert_ride(create_ride)
    return create_ride

@pytest.fixture
def from_coord() -> CoordinateEntitie:
    return CoordinateEntitie(latitude=-23.509698, longitude=-46.6587042).object()


@pytest.fixture
def to_coord() -> CoordinateEntitie:
    return CoordinateEntitie(latitude=-23.5200384, longitude=-46.6682877).object()


def test_ride_is_not_passenger(account_not_passenger, from_coord, to_coord):
    with pytest.raises(ErrorIsNeedPassenger):
        use_case = Route(ride_repository=ride_repository, passenger_repository=account_repository)
        use_case.create_new_route(
            account_id=account_not_passenger.account_id, from_coordinate=from_coord, to_coordinate=to_coord
        )


def test_passenger_have_other_ride_in_progress(
    account_passenger, ride_in_progress, from_coord, to_coord
):
    with pytest.raises(ErrorHaveRideInProgress):
        use_case = Route(ride_repository=ride_repository, passenger_repository=account_repository)
        use_case.create_new_route(
            account_id=account_passenger.account_id, from_coordinate=from_coord, to_coordinate=to_coord
        )


def test_new_ride(account_passenger, from_coord, to_coord):
    use_case = Route(ride_repository=ride_repository, passenger_repository=account_repository)
    ride = use_case.create_new_route(
        account_id=account_passenger.account_id, from_coordinate=from_coord, to_coordinate=to_coord
    )
    assert ride.status == RideStatusEnum.CREATED.value
