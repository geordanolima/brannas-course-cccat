from uuid import uuid4

import pytest

from src.domain.models import Account
from src.presenter.errors import (
    ErrorAccountExistent,
    ErrorInvalidCpf,
    ErrorInvalidEmail,
    ErrorInvalidName,
    ErrorInvalidPlate,
)
from src.repositories.tests import AccountTestRepository
from src.use_case import Signup

@pytest.fixture
def create_account() -> Account:
    account = Account(
        account_id=str(uuid4()),
        name="test name",
        email="test@test.com",
        password="12345",
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
    )
    return account


@pytest.fixture
def create_account_invalid_name(create_account) -> Account:
    account = create_account
    account.email = "testname@test.com"
    account.name = "test_name"
    return account


@pytest.fixture
def create_account_invalid_email(create_account) -> Account:
    account = create_account
    account.email = "testtest.com"
    return account


@pytest.fixture
def create_account_invalid_cpf(create_account) -> Account:
    account = create_account
    account.email = "testcpf@test.com"
    account.cpf = '123.123.123-12'
    return account


@pytest.fixture
def create_account_invalid_plate(create_account) -> Account:
    account = create_account
    account.email = "testcarplate@test.com"
    account.is_driver = True
    account.car_plate = "1234-ABC"
    return account


@pytest.fixture
def populate_account(repository, create_account: Account):
    account = create_account
    account.email = "testexistent@test.com"
    repository.insert_account(account=account)
    return account


@pytest.fixture
def repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


def test_account_existent(populate_account, repository):
    with pytest.raises(ErrorAccountExistent):
        signup = Signup(repository=repository)
        signup.sigin(account=populate_account)


def test_account_not_existent(repository, create_account):
    signup = Signup(repository=repository)
    registered: Account = signup.sigin(account=create_account)
    id = repository.get_account_by_id(id=registered.account_id).account_id
    assert registered.account_id == id


def test_account_invalid_name(repository, create_account_invalid_name):
    with pytest.raises(ErrorInvalidName):
        signup = Signup(repository=repository)
        signup.sigin(account=create_account_invalid_name)


def test_account_invalid_email(create_account_invalid_email, repository):
    with pytest.raises(ErrorInvalidEmail):
        signup = Signup(repository=repository)
        signup.sigin(account=create_account_invalid_email)


def test_account_invalid_cpf(create_account_invalid_cpf, repository):
    with pytest.raises(ErrorInvalidCpf):
        signup = Signup(repository=repository)
        signup.sigin(account=create_account_invalid_cpf)


def test_account_driver_invalid_plate(create_account_invalid_plate, repository):
    with pytest.raises(ErrorInvalidPlate):
        signup = Signup(repository=repository)
        signup.sigin(account=create_account_invalid_plate)
