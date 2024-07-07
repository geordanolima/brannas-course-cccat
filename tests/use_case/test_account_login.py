from uuid import uuid4

import pytest

from src.repositories.tests import AccountTestRepository
from src.domain.models import Account
from src.presenter import ErrorLoginIncorrect
from src.use_case import Login


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
def populate_account(repository, create_account: Account):
    return repository.insert_account(account=create_account)


@pytest.fixture
def repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


def test_account_not_exists(create_account, repository):
    with pytest.raises(ErrorLoginIncorrect):
        login = Login(repository=repository)
        login.run(email=create_account.email, password=create_account.password)


def test_password_incorrect(populate_account, repository):
    with pytest.raises(ErrorLoginIncorrect):
        login = Login(repository=repository)
        login.run(email=populate_account.email, password=f"fail-{populate_account.password}")


def test_login_success(repository, populate_account, create_account):
    login = Login(repository=repository)
    account = login.run(email=create_account.email, password=create_account.password)
    assert account.account_id == populate_account.account_id
