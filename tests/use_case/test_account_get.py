from uuid import uuid4

import pytest

from src.domain.models import Account
from src.repositories.tests import AccountTestRepository
from src.presenter import ErrorIsInvalidUUID
from src.use_case.account_get import AccountGet


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
