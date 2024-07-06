from ..repositories.account_db_repository import AccountDatabaseRepository
from ..domain.models import Account, LoginRequest
from ..presenter import BasePresenter
from ..provider import DatabaseProvider
from ..use_case.signup import Signup
from ..presenter.errors import BaseException


class AccountController:
    def __init__(self) -> None:
        self._repository = AccountDatabaseRepository(db=DatabaseProvider().connection)
        self.presenter = BasePresenter()
        self.use_case = Signup(repository=self._repository)

    def create_account(self, account: Account):
        try:
            result = self.use_case.sigin(account=account)
            return self.presenter.response(result.dict())
        except BaseException as error:
            return self.presenter.response_error(error)

    def login(self, login: LoginRequest):
        try:
            result = self.use_case.login(email=login.email, password=login.password)
            return self.presenter.response(result.dict())
        except BaseException as error:
            return self.presenter.response_error(error)
    
    def get_account_by_id(self, account_id: str):
        try:
            result = self.use_case.get_account_by_id(account_id=account_id)
            return self.presenter.response(result.dict())
        except BaseException as error:
            return self.presenter.response_error(error)
