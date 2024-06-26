from uuid import uuid4
import pytest
from src.repositories.account import AccountRepository
from src.models.account import Account
from src.use_case.signup import Signup
from src.utils.errors import (
    ErrorAccountExistent,
    ErrorInvalidCpf,
    ErrorInvalidEmail,
    ErrorInvalidName,
    ErrorInvalidPlate,
)


@pytest.fixture
def create_account() -> Account:
    account = Account(
        account_id=str(uuid4()),
        name = "test name",
        email = "test@test.com",
        cpf = "857.306.180-42",
        is_passenger = True,
        is_driver = False,
        car_plate = "",
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
def populate_account(db_session, create_account: Account):
    account = create_account
    account.email = "testexistent@test.com"
    db_session.execute(AccountRepository(account).sql_create_account())
    return account


def test_account_existent(populate_account, db_connection):
    with pytest.raises(ErrorAccountExistent):
        signup = Signup(connection_db=db_connection)
        signup.sigin(account=populate_account)


def test_account_not_existent(create_account, db_connection):
    signup = Signup(connection_db=db_connection)
    registered: Account = signup.sigin(account=create_account)
    id = db_connection.db_get(sql=AccountRepository().get_account_id(id=create_account.account_id))[0][0]
    assert registered.account_id == id
    
    
def test_account_invalid_name(create_account_invalid_name, db_connection):
    with pytest.raises(ErrorInvalidName):
        signup = Signup(connection_db=db_connection)
        signup.sigin(account=create_account_invalid_name)


def test_account_invalid_email(create_account_invalid_email, db_connection):
    with pytest.raises(ErrorInvalidEmail):
        signup = Signup(connection_db=db_connection)
        signup.sigin(account=create_account_invalid_email)


def test_account_invalid_cpf(create_account_invalid_cpf, db_connection):
    with pytest.raises(ErrorInvalidCpf):
        signup = Signup(connection_db=db_connection)
        signup.sigin(account=create_account_invalid_cpf)


def test_account_driver_invalid_plate(create_account_invalid_plate, db_connection):
    with pytest.raises(ErrorInvalidPlate):
        signup = Signup(connection_db=db_connection)
        signup.sigin(account=create_account_invalid_plate)
