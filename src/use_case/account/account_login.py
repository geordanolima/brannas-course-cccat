from src.domain.repositories import AccountRepository
from src.presenter import ErrorLoginIncorrect
from src.domain.value_objects import PasswordObject
from src.use_case import BaseUseCase


class Login(BaseUseCase):
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository = account_repository
        self._password = PasswordObject()

    def run(self, email: str, password: str):
        account = self._account_repository.get_account_by_email(email=email, hide_password=False)
        if not account or not self._validate_password(account_password=account.password, password=password):
            raise ErrorLoginIncorrect()
        return account

    def _validate_password(self, account_password, password) -> bool:
        return self._password.compare_password(hashed_password=account_password.encode(), password=password)
