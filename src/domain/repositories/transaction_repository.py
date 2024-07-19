import abc

from src.domain.models import Transaction
from src.database import Database


class TransactionRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db: Database) -> None:
        ...

    @abc.abstractmethod
    def insert_transaction(self, transaction: Transaction) -> Transaction:
        ...

    @abc.abstractmethod
    def get_transaction(self, transaction_id: str):
        ...