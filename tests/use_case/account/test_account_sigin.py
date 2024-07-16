import pytest

from src.domain.models import Account
from src.presenter.errors import (
    ErrorAccountExistent,
    ErrorInvalidCpf,
    ErrorInvalidEmail,
    ErrorInvalidName,
    ErrorInvalidPlate,
)
from src.use_case import Sigin


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


def test_account_existent(populate_account, repository):
    with pytest.raises(ErrorAccountExistent):
        use_case = Sigin(repository=repository)
        use_case.run(account=populate_account)


def test_account_not_existent(repository, create_account):
    use_case = Sigin(repository=repository)
    registered: Account = use_case.run(account=create_account)
    id = repository.get_account_by_id(id=registered.account_id).account_id
    assert registered.account_id == id


def test_account_invalid_name(repository, create_account_invalid_name):
    with pytest.raises(ErrorInvalidName):
        use_case = Sigin(repository=repository)
        use_case.run(account=create_account_invalid_name)


def test_account_invalid_email(create_account_invalid_email, repository):
    with pytest.raises(ErrorInvalidEmail):
        use_case = Sigin(repository=repository)
        use_case.run(account=create_account_invalid_email)


def test_account_invalid_cpf(create_account_invalid_cpf, repository):
    with pytest.raises(ErrorInvalidCpf):
        use_case = Sigin(repository=repository)
        use_case.run(account=create_account_invalid_cpf)


def test_account_driver_invalid_plate(create_account_invalid_plate, repository):
    with pytest.raises(ErrorInvalidPlate):
        use_case = Sigin(repository=repository)
        use_case.run(account=create_account_invalid_plate)
