import re

from curso_brannas.src.utils.validates import Validate
from .models.account import Account
from .repositories.account import AccountRepository
from .utils.errors import Errors
from curso_brannas.src.database import Database

class Signup():
    def __init__(self, connection_db: Database) -> None:
        self.db = connection_db
        self.validate = Validate()
    
    def sigin(self, account: Account):
        if self._validate_account_existent(email=account.email):
            return Errors.ACCOUNT_EXISTENT
        if self.validate.invalid_account_name(name=account.name):
            return Errors.INVALID_NAME
        if self.validate.invalid_account_email(email=account.email):
            return Errors.INVALID_EMAIL
        if self.validate.invalid_account_cpf(cpf=account.cpf):
            return Errors.INVALID_CPF
        if account.is_driver and self.validate.invalid_account_plate(plate=account.car_plate):
            return Errors.INVALID_PLATE
        self._create_account(account=account)
        return self._get_id_account(email=account.email)

    def _validate_account_existent(self, email: Account):
        return self.db.db_get(sql=AccountRepository().get_exists_account(email=email))[0][0]

    def _create_account(self, account: Account):
        self.db.db_query(sql=AccountRepository(account).sql_create_account())
    
    def _get_id_account(self, email):
        account = self.db.db_get(sql=AccountRepository().get_account(email=email))
        if account:
            return account[0][0]
        return None
