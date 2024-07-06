from uuid import uuid4

from ..utils.passwords import compare_password, cryptography_password

from ..domain.models import Account
from ..domain.entities import Cpf, AccountEntitie
from ..domain.repositories import AccountRepository
from ..utils import (
    ErrorAccountExistent,
    ErrorInvalidEmail,
    ErrorInvalidName,
    ErrorInvalidPlate,
    ErrorIsInvalidUUID,
    ErrorLoginIncorrect,
    Validates,
)


class Signup:
    def __init__(self, repository: AccountRepository) -> None:
        self.validate = Validates()
        self.repository = repository

    def sigin(self, account: AccountEntitie) -> Account:
        if self.repository.get_exists_account(email=account.email):
            raise ErrorAccountExistent()
        if self.validate.invalid_name(name=account.name):
            raise ErrorInvalidName()
        if self.validate.invalid_email(email=account.email):
            raise ErrorInvalidEmail()
        if self.validate.invalid_plate(plate=account.car_plate, is_driver=account.is_driver):
            raise ErrorInvalidPlate()
        account.cpf = Cpf(account.cpf).get_cpf()
        account.account_id = uuid4()
        account.password = cryptography_password(password=account.password)
        self.repository.insert_account(account=account)
        return self.repository.get_account_by_id(id=account.account_id)

    def login(self, email: str, password: str):
        account = self.repository.get_account_by_email(email=email, hide_password=False)
        if not account or not compare_password(hashed_password=account.password.encode(), password=password):
            raise ErrorLoginIncorrect()
        return account

    def get_account_by_id(self, account_id: str) -> Account:
        account = self.repository.get_account_by_id(id=account_id)
        if not account:
            raise ErrorIsInvalidUUID()
        return account