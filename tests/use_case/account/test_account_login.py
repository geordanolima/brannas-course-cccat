import pytest

from src.presenter import ErrorLoginIncorrect
from src.use_case import Login


def test_account_not_exists(account_entitie, account_repository):
    with pytest.raises(ErrorLoginIncorrect):
        use_case = Login(account_repository=account_repository)
        use_case.run(email=account_entitie.email, password=account_entitie.password)


def test_password_incorrect(create_account, account_repository):
    with pytest.raises(ErrorLoginIncorrect):
        use_case = Login(account_repository=account_repository)
        use_case.run(email=create_account.email, password=f"fail-{create_account.password}")


def test_login_success(account_repository, populate_account_entitie, account_entitie, password):
    use_case = Login(account_repository=account_repository)
    _account = use_case.run(email=account_entitie.email, password=password)
    assert _account.account_id == account_entitie.account_id
