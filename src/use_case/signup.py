from uuid import uuid4

from ..domain.models import Account
from ..repositories import AccountRepository
from ..utils import (
    ErrorAccountExistent, ErrorInvalidCpf, ErrorInvalidEmail, ErrorInvalidName, ErrorInvalidPlate, Validates
)


class Signup:
    def __init__(self, repository: AccountRepository) -> None:
        self.validate = Validates()
        self.repository = repository

    def sigin(self, account: Account) -> Account:
        if self.repository.get_exists_account(email=account.email):
            raise ErrorAccountExistent()
        if self.validate.invalid_name(name=account.name):
            raise ErrorInvalidName()
        if self.validate.invalid_email(email=account.email):
            raise ErrorInvalidEmail()
        if self.validate.invalid_cpf(cpf=account.cpf):
            raise ErrorInvalidCpf()
        if self.validate.invalid_plate(plate=account, is_driver=account.is_driver):
            raise ErrorInvalidPlate()
        account.account_id = uuid4()
        self.repository.insert_account(account=account)
        return self.repository.get_account_by_id(id=account.account_id)
