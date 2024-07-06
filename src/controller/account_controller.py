from ..repositories.account_db_repository import AccountDatabaseRepository
from ..domain.models import Account, LoginRequest
from ..presenter import BasePresenter
from ..provider import DatabaseProvider
from ..use_case.signup import Signup
from ..presenter.errors import BaseException


class AccountController:
    def __init__(self) -> None:
        self._repository = AccountDatabaseRepository(db=DatabaseProvider().connection)
        self._presenter = BasePresenter().exception_handler
        self.use_case = Signup(repository=self._repository)

    def create_account(self, account: Account):
        return self._presenter(method=self.use_case.sigin, params={account})

    def login(self, login: LoginRequest):
        return self._presenter(method=self.use_case.login, params={login.email, login.password})
    
    def get_account_by_id(self, account_id: str):
        return self._presenter(method=self.use_case.get_account_by_id, params={account_id})

