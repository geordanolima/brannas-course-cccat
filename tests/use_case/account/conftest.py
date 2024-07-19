from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.entities import AccountEntitie
from src.domain.models import Account
from tests.repositories import AccountTestRepository


@pytest.fixture
def account_repository() -> AccountTestRepository:
    return AccountTestRepository(db=None)


@pytest.fixture
def password():
    return "Senha@segura123"


@pytest.fixture
def create_account(password) -> Account:
    account = Account(
        account_id=str(uuid4()),
        name="test name",
        email="test@test.com",
        password=password,
        cpf="857.306.180-42",
        is_passenger=True,
        is_driver=False,
        car_plate="",
        rate=-1,
        created_at=datetime.now().isoformat()
    )
    return account


@pytest.fixture
def populate_account(account_repository, create_account: Account) -> Account:
    return account_repository.insert_account(account=create_account)


@pytest.fixture
def account_entitie(create_account) -> Account:
    return AccountEntitie(**create_account.dict()).object()


@pytest.fixture
def populate_account_entitie(account_repository, account_entitie: Account) -> Account:
    return account_repository.insert_account(account=account_entitie)
