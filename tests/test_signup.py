import pytest
from curso_brannas.src.repositories.account import AccountRepository
from curso_brannas.src.models.account import Account
from curso_brannas.src.signup import Signup
from curso_brannas.src.utils.errors import Errors


@pytest.fixture
def create_account() -> Account:
    account = Account()
    account.new(
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
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=populate_account)
    assert registered == Errors.ACCOUNT_EXISTENT


def test_account_not_existent(create_account, db_connection):
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=create_account)
    id = db_connection.db_get(sql=AccountRepository().get_account(email=create_account.email))[0][0]
    assert registered == id
    
    
def test_account_invalid_name(db_clear, create_account_invalid_name, db_connection):
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=create_account_invalid_name)
    assert registered == Errors.INVALID_NAME


def test_account_invalid_email(create_account_invalid_email, db_connection):
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=create_account_invalid_email)
    assert registered == Errors.INVALID_EMAIL


def test_account_invalid_cpf(create_account_invalid_cpf, db_connection):
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=create_account_invalid_cpf)
    assert registered == Errors.INVALID_CPF
    
def test_account_driver_invalid_plate(create_account_invalid_plate, db_connection):
    signup = Signup(connection_db=db_connection)
    registered = signup.sigin(account=create_account_invalid_plate)
    assert registered == Errors.INVALID_PLATE
