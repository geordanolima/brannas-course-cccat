from src.database import Database
from src.domain.models.account import Account
from src.domain.repositories import AccountRepository


class AccountTestRepository(AccountRepository):
    def __init__(self, db: Database = None) -> None:
        self.db = db
        self.accounts: list[Account] = []

    def insert_account(self, account: Account):
        self.accounts.append(account)
        return account

    def get_account_by_email(self, email: str) -> Account:
        for account in self.accounts:
            if account.email == email:
                return account

    def get_account_by_id(self, id: str) -> Account:
        for account in self.accounts:
            if account.account_id == id:
                return account

    def get_accounts(self, limit: int = None) -> list[Account]:
        return self.accounts[:limit]

    def get_exists_account(self, email: str) -> bool:
        return bool(self.get_account_by_email(email=email))

    def update_account(self, account_id: str, new_account: Account):
        account = self.get_account_by_id(id=account_id)
        if account:
            account.name = new_account.name
            account.car_plate = new_account.car_plate
            account.is_passenger = new_account.is_passenger
            account.is_driver = new_account.is_driver

    def update_password(self, account_id: str, new_password: str):
        account = self.get_account_by_id(id=account_id)
        if account:
            account.password = new_password
