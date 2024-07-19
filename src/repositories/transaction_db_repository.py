from database import Database
from domain.models.transaction import Transaction
from settings import Settings
from src.domain.repositories import TransactionRepository


class TransactionDatabaseRepository(TransactionRepository):
    table = "{}.transaction".format(Settings().DATABASE_SCHEMA)
    def __init__(self, db: Database) -> None:
        self._db = db

    def insert_transaction(self, transaction: Transaction) -> Transaction:
        self._db.db_query(sql=self._sql_insert_transaction(transaction=transaction))
        
    def get_transaction(self, transaction_id: str):
        self._db.db_get_dict(sql=self._sql_get_transaction(transaction_id=transaction_id))

    def _sql_insert_transaction(self, transaction: Transaction) -> str:
        sql = """INSERT INTO {table} (transaction_id, ride_id, amount, satus, created_at)
        values ('{transaction_id}'::uuid, '{ride_id}'::uuid, {amount}, {status}, '{created_at}')"""
        return sql.format(
            table=self.table,
            transaction_id=transaction.transaction_id,
            ride_id=transaction.ride_id,
            amount=transaction.amount,
            status=transaction.status,
            created_at=transaction.created_at,
        )

    def _sql_get_transacttion(self, transaction_id: str) -> str:
        sql = """SELECT * FROM {table} WHERE transaction_id = {transaction_id};"""
        return sql.format(table=self.table, transaction_id=transaction_id)
