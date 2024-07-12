from src.domain.models import Account
from src.domain.repositories import AccountRepository
from src.presenter import ErrorIsInvalidUUID
from src.utils.validates import Validates


class AccountGet:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository
        self._validate = Validates()

    def get_account_by_id(self, account_id: str) -> Account:
        if not self._validate.is_uuid(id=account_id):
            raise ErrorIsInvalidUUID()
        account = self._repository.get_account_by_id(id=account_id)
        if not account:
            raise ErrorIsInvalidUUID()
        return account
