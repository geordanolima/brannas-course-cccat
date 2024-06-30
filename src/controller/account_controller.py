from ..repositories.account_db_repository import AccountDatabaseRepository
from ..domain.models import Account
from ..presenter import BasePresenter
from ..provider import DatabaseProvider
from ..use_case.signup import Signup
from ..utils.errors import BaseException


class AccountController:
    def __init__(self) -> None:
        self._repository = AccountDatabaseRepository(db=DatabaseProvider().connection)
        self.presenter = BasePresenter()

    def run(self, account: Account):
        use_case = Signup(repository=self._repository)
        try:
            result = use_case.sigin(account=account)
            return self.presenter.response(result.dict())
        except BaseException as error:
            return self.presenter.response_error(error)
