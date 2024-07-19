import pytest

from src.presenter import ErrorIsInvalidUUID
from src.use_case import AccountGet


def test_get_account_not_exists(create_account, account_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = AccountGet(account_repository=account_repository)
        use_case.get_id(id=create_account.account_id)


def test_get_account_success(populate_account, account_repository):
    use_case = AccountGet(account_repository=account_repository)
    use_case.get_id(id=populate_account.account_id)
