from src.domain.models import Account
from src.domain.entities import AccountEntitie
from src.domain.repositories import AccountRepository
from src.presenter import ErrorAccountExistent
from src.use_case import BaseUseCase


class Sigin(BaseUseCase):
    def __init__(self, repository: AccountRepository) -> None:
        self.repository = repository

    def run(self, account: Account) -> Account:
        if self.repository.get_exists_account(email=account.email):
            raise ErrorAccountExistent()
        account = AccountEntitie(**account.dict()).object()
        self.repository.insert_account(account=account)
        return self.repository.get_account_by_id(id=account.account_id)
