from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.models import Account
from src.presenter import ErrorIsInvalidUUID
from src.use_case import AccountGet
from tests.repositories import AccountTestRepository


@pytest.fixture
def create_account() -> Account:
    account = Account(
        account_id=str(uuid4()),
        name="test name",
        email="test@test.com",
        password="Senha@segura123",
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
        created_at=datetime.now()
    )
    return account


@pytest.fixture
def populate_account(repository, create_account: Account) -> Account:
    return repository.insert_account(account=create_account)


@pytest.fixture
def repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


def test_get_account_not_exists(create_account, repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = AccountGet(repository=repository)
        use_case.get_account_by_id(account_id=create_account.account_id)


def test_get_account_success(populate_account, repository):
    use_case = AccountGet(repository=repository)
    use_case.get_account_by_id(account_id=populate_account.account_id)
