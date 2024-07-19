from datetime import datetime
import pytest

from src.domain.models import Account, LoginRequest
from src.provider import DatabaseProvider
from src.controller import AccountController


@pytest.fixture
def account_controller(mocker, db_connection) -> AccountController:
    mocker.patch.object(DatabaseProvider, "get_connection", return_value=db_connection,)
    return AccountController()


@pytest.fixture
def password():
    return "Senha@segura123"


@pytest.fixture
def account(password):
    return Account(
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
def login(password) -> LoginRequest:
    return LoginRequest(email="test@test.com", password=password)


@pytest.fixture
def login_invalid() -> LoginRequest:
    return LoginRequest(email="test@test.com", password="password")