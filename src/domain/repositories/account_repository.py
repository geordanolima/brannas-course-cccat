import abc

from src.database import Database
from src.domain.models import Account


class AccountRepository(abc.ABC):

    @abc.abstractmethod
    def __init__(self, db: Database) -> None:
        ...

    @abc.abstractmethod
    def insert_account(self, account: Account):
        ...

    @abc.abstractmethod
    def get_exists_account(self, email: str) -> bool:
        ...

    @abc.abstractmethod
    def get_account_by_email(self, email: str, hide_password: bool = True) -> Account:
        ...

    @abc.abstractmethod
    def get_account_by_id(self, id) -> Account:
        ...

    @abc.abstractmethod
    def get_accounts(self, limit: int = None) -> list[Account]:
        ...

    @abc.abstractmethod
    def update_account(self, new_account: Account):
        ...

    @abc.abstractmethod
    def update_password(self, new_password):
        ...
