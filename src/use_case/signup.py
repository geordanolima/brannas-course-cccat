from src.database import Database
from src.models.account import Account, AccountDict
from src.presenter.base_presenter import BasePresenter
from src.repositories.account import AccountRepository
from src.utils.validates import Validate
from src.utils.errors import ErrorAccountExistent, ErrorInvalidCpf, ErrorInvalidEmail, ErrorInvalidName, ErrorInvalidPlate

class Signup():
    def __init__(self, connection_db: Database) -> None:
        self.db = connection_db
        self.validate = Validate()
    
    def sigin(self, account: Account) -> Account:
        if self._validate_account_existent(email=account.email):
            raise ErrorAccountExistent()
        if self.validate.invalid_account_name(name=account.name):
            raise ErrorInvalidName()
        if self.validate.invalid_account_email(email=account.email):
            raise ErrorInvalidEmail()
        if self.validate.invalid_account_cpf(cpf=account.cpf):
            raise ErrorInvalidCpf()
        if account.is_driver and self.validate.invalid_account_plate(plate=account.car_plate):
            raise ErrorInvalidPlate()
        account.account_id = account.get_id()
        self._create_account(account=account)
        return self._get_id_account_id(id=account.account_id)

    def _validate_account_existent(self, email: Account):
        return self.db.db_get(sql=AccountRepository().get_exists_account(email=email))[0][0]

    def _create_account(self, account: Account):
        return self.db.db_query(sql=AccountRepository(account).sql_create_account())
    
    def _get_id_account_id(self, id):
        accounts = self.db.db_get_dict(sql=AccountRepository().get_account_id(id=id))
        if accounts:
            return AccountDict(**accounts[0]).account()
        return None

    def _get_list_accounts(self):
        accounts = self.db.db_get_dict(sql=AccountRepository().get_accounts(limit=100))
        result = []
        for item in accounts:
            result.append(AccountDict(**item).account())
        return result
