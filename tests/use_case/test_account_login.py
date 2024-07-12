from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.entities import AccountEntitie
from src.domain.models import Account
from src.presenter import ErrorLoginIncorrect
from src.use_case import Login
from tests.repositories import AccountTestRepository


@pytest.fixture
def password():
    return "Senha@segura123"


@pytest.fixture
def create_account(password) -> Account:
    return AccountEntitie(
        account_id=str(uuid4()),
        name="test name",
        email="test@test.com",
        password=password,
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
        created_at=datetime.now()
    ).object()


@pytest.fixture
def populate_account(repository, create_account: Account):
    return repository.insert_account(account=create_account)


@pytest.fixture
def repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


def test_account_not_exists(create_account, repository):
    with pytest.raises(ErrorLoginIncorrect):
        use_case = Login(repository=repository)
        use_case.run(email=create_account.email, password=create_account.password)


def test_password_incorrect(populate_account, repository):
    with pytest.raises(ErrorLoginIncorrect):
        use_case = Login(repository=repository)
        use_case.run(email=populate_account.email, password=f"fail-{populate_account.password}")


def test_login_success(repository, populate_account, create_account, password):
    use_case = Login(repository=repository)
    account = use_case.run(email=create_account.email, password=password)
    assert account.account_id == populate_account.account_id
