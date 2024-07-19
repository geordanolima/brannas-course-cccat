from src.domain.models import Account
from src.domain.entities import AccountEntitie
from src.domain.repositories import AccountRepository
from src.presenter import ErrorAccountExistent
from src.use_case import BaseUseCase


class Sigin(BaseUseCase):
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository

    def run(self, account: Account) -> Account:
        if self._account_repository.get_exists_account(email=account.email):
            raise ErrorAccountExistent()
        account = AccountEntitie(**account.dict()).object()
        return self._account_repository.insert_account(account=account)
