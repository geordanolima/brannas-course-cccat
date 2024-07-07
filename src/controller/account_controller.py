from ..repositories.account_db_repository import AccountDatabaseRepository
from ..domain.models import Account, LoginRequest
from ..presenter import BasePresenter
from ..provider import DatabaseProvider
from ..use_case.account_login import UCAccount
from ..presenter.errors import BaseException


class AccountController:
    def __init__(self) -> None:
        self._repository = AccountDatabaseRepository(db=DatabaseProvider().connection)
        self._presenter = BasePresenter()
        self.use_case = UCAccount(repository=self._repository)

    def create_account(self, account: Account):
        try:
            result = self.use_case.sigin(account=account)
            return self._presenter.response(result.dict())
        except BaseException as error:
            return self._presenter.response_error(error)

    def login(self, login: LoginRequest):
        return self._presenter.exception_handler(method=self.use_case.login, params={login.email, login.password})

    def get_account_by_id(self, account_id: str):
        return self._presenter.exception_handler(method=self.use_case.get_account_by_id, params={account_id})
