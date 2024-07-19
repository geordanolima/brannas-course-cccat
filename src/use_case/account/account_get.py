from src.domain.models import Account
from src.domain.repositories import AccountRepository
from src.presenter import ErrorIsInvalidUUID
from src.use_case import BaseGetUseCase


class AccountGet(BaseGetUseCase):
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    def get_id(self, id: str) -> Account:
        super().get_id(id=id)
        account = self._account_repository.get_account_by_id(id=id)
        if not account:
            raise ErrorIsInvalidUUID()
        return account
