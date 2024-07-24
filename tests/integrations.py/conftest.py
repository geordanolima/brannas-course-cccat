from datetime import datetime
from uuid import uuid4
import pytest

from src.repositories import AccountDatabaseRepository
from src.domain.models import Account, Coordinate, LoginRequest
from src.provider import DatabaseProvider
from src.controller import AccountController, RideController


@pytest.fixture
def account_controller(mocker, db_connection) -> AccountController:
    mocker.patch.object(DatabaseProvider, "get_connection", return_value=db_connection,)
    return AccountController()


@pytest.fixture
def ride_controller(mocker, db_connection) -> RideController:
    mocker.patch.object(DatabaseProvider, "get_connection", return_value=db_connection,)
    return RideController()


@pytest.fixture
def password():
    return "Senha@segura123"


@pytest.fixture
def account(password):
    return Account(
        account_id="3836f7c1-bd6d-415e-af8a-a6157d6b6270",
        name="test name",
        email="test@test.com",
        password=password,
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
        rate=0,
        created_at=datetime(day=18, month=7, year=2024, hour=21, minute=40, second=0).isoformat()
    )


@pytest.fixture
def account_repository(db_connection) -> AccountDatabaseRepository:
    return AccountDatabaseRepository(db=db_connection)


@pytest.fixture
def populate_account(account_repository, account: Account) -> Account:
    return account_repository.insert_account(account=account)


@pytest.fixture
def populate_account_driver(account_repository, account: Account) -> Account:
    account_driver = Account(**account.dict())
    account_driver.account_id = uuid4()
    account_driver.is_driver = True
    account_driver.is_passenger = False
    account_driver.car_plate = 'ABC-1234'    
    return account_repository.insert_account(account=account_driver)


@pytest.fixture
def login(password) -> LoginRequest:
    return LoginRequest(email="test@test.com", password=password)


@pytest.fixture
def login_invalid() -> LoginRequest:
    return LoginRequest(email="test@test.com", password="password")


@pytest.fixture
def from_coordinate() -> Coordinate:
    return Coordinate(latitude=-91.39393, longitude=-2.122)


@pytest.fixture
def to_coordinate() -> Coordinate:
    return Coordinate(latitude=-89.39393, longitude=183.122)

@pytest.fixture
def positions(from_coordinate, to_coordinate) -> list[Coordinate]:
    return [
        from_coordinate,
        Coordinate(latitude=91.39393, longitude=-2.122),
        Coordinate(latitude=-89.39393, longitude=-183.122),
        to_coordinate,
    ]
