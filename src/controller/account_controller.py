from ..repositories.account_db_repository import AccountDatabaseRepository
from ..domain.models import Account, LoginRequest
from ..presenter import BasePresenter
from ..provider import DatabaseProvider
from ..use_case import AccountGet, Login, Sigin
from ..presenter.errors import BaseException


class AccountController:
    def __init__(self) -> None:
        self._repository = AccountDatabaseRepository(db=DatabaseProvider().connection)
        self._presenter = BasePresenter()

    def create_account(self, account: Account):
        use_case = Sigin(repository=self._repository)
        try:
            result = use_case.run(account=account)
            return self._presenter.response(result.dict())
        except BaseException as error:
            return self._presenter.response_error(error)

    def login(self, login: LoginRequest):
        use_case = Login(repository=self._repository)
        return self._presenter.exception_handler(method=use_case.login, params={login.email, login.password})

    def get_account_by_id(self, id: str):
        use_case = AccountGet(repository=self._repository)
        return self._presenter.exception_handler(method=use_case.get_id, params={id})
