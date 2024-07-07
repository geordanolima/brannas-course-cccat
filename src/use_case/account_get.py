from src.domain.models import Account
from src.domain.repositories import AccountRepository
from src.presenter import ErrorIsInvalidUUID


class AccountGet:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    def get_account_by_id(self, account_id: str) -> Account:
        account = self._repository.get_account_by_id(id=account_id)
        if not account:
            raise ErrorIsInvalidUUID()
        return account
