from ..presenter.base_presenter import BasePresenter
from ..database import Database
from ..models.account import Account
from settings import Settings
from ..use_case.signup import Signup
from src.utils.errors import BaseException


class AccountController():
    def __init__(self) -> None:
        self.settings = Settings()
        self.database = Database(
            host=self.settings.DATABASE_HOST,
            port=self.settings.DATABASE_PORT,
            db_name=self.settings.DATABASE_NAME,
            user=self.settings.DATABASE_USER,
            password=self.settings.DATABASE_PASS,
        )
        self.presenter = BasePresenter()
    
    def run(self, account: Account):
        use_case = Signup(connection_db=self.database)
        try:
            result = use_case.sigin(account=account)
            return self.presenter.response(result.dict())
        except BaseException as error:
            return self.presenter.response_error(error)
