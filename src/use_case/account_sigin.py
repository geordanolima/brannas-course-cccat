from ..domain.models import Account
from ..domain.entities import AccountEntitie
from ..domain.repositories import AccountRepository
from ..presenter import ErrorAccountExistent
from ..utils import Validates


class Sigin:
    def __init__(self, repository: AccountRepository) -> None:
        self.validate = Validates()
        self.repository = repository

    def run(self, account: Account) -> Account:
        if self.repository.get_exists_account(email=account.email):
            raise ErrorAccountExistent()
        account = AccountEntitie(**account.dict()).object()
        self.repository.insert_account(account=account)
        return self.repository.get_account_by_id(id=account.account_id)
