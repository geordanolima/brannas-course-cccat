from src.database import Database
from src.domain.models import Transaction
from src.domain.repositories import TransactionRepository


class TransactionTestRepository(TransactionRepository):
    def __init__(self, db: Database = None) -> None:
        self._db = db
        self._transactions = []

    def insert_transaction(self, transaction: Transaction) -> Transaction:
        self._transactions.append(transaction)
        return transaction
    
    def get_transaction(self, transaction_id: str):
        for transaction in self._transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None
