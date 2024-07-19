from datetime import datetime

from settings import Settings
from src.database import Database
from src.domain.entities import AccountEntitie
from src.domain.models import Account
from src.domain.repositories import AccountRepository


class AccountDatabaseRepository(AccountRepository):
    table: str = "{}.account".format(Settings().DATABASE_SCHEMA)

    def __init__(self, db: Database) -> None:
        self.db = db

    def insert_account(self, account: Account):
        self.db.db_query(sql=self._sql_insert_account(account=account))
        return self.get_account_by_id(id=account.account_id)

    def get_exists_account(self, email: str) -> bool:
        return bool(self.db.db_get(sql=self._sql_get_exists_account(email=email))[0][0])

    def get_account_by_email(self, email, hide_password: bool = True):
        account = self.db.db_get_dict(self._sql_get_account_by_email(email=email))
        if account:
            return self._get_obj_account(account=account[0], hide_password=hide_password)
        return None

    def get_account_by_id(self, id):
        accounts = self.db.db_get_dict(sql=self._sql_get_account_by_id(id=id))
        if accounts:
            account = accounts[0]
            account["password"] = "Password#123"
            return self._get_obj_account(account=account, hide_password=True)
        return None

    def get_accounts(self):
        accounts = self.db.db_get_dict(sql=self._sql_get_accounts(limit=100))
        result = []
        for item in accounts:
            result.append(self._get_obj_account(account=item, hide_password=True))
        return result

    def update_account(self, account: Account, new_account: Account):
        return self.db.db_query(sql=self._sql_update_account(account=account, new_account=new_account))

    def update_password(self, account: Account, new_password: str):
        return self.db.db_query(sql=self._sql_update_password(account=account, new_password=new_password))

    def _get_obj_account(self, account: dict, hide_password: bool):
        updated_values = {"load_db": True}
        for item in account:
            if isinstance(account[item], datetime):
                updated_values[item] = account[item].isoformat()
            else:
                updated_values[item] = account[item]
        return AccountEntitie(**updated_values).object(hide_password=hide_password)
            

    def _sql_insert_account(self, account: Account) -> str:
        sql = """INSERT INTO {table}
            (account_id, "name", email, password, cpf, car_plate, is_passenger, is_driver, created_at, updated_at)
        VALUES ('{account_id}', '{name}', '{email}', '{password}',
            '{cpf}', '{car_plate}', {is_passenger}, {is_driver}, '{created_at}', Null);
        """
        return sql.format(
            table=self.table,
            account_id=account.account_id,
            name=account.name,
            email=account.email,
            password=account.password,
            cpf=account.cpf,
            car_plate=account.car_plate,
            is_passenger=account.is_passenger,
            is_driver=account.is_driver,
            created_at=datetime.now(),
        )

    def _sql_get_exists_account(self, email):
        return f"select count(1) from {self.table} where email = '{email}';"

    def _sql_get_account_by_email(self, email):
        return f"select * from {self.table} where email = '{email}';"

    def _sql_get_account_by_id(self, id):
        return f"select * from {self.table} where account_id = '{id}';"

    def _sql_get_accounts(self, limit: int = None):
        query_limit = ""
        if limit:
            query_limit = f"LIMIT {limit}"
        return f"select * from {self.table} {query_limit}';"

    def _sql_update_account(self, account: Account, new_account: Account):
        sql = """
            UPDATE {table} SET
                "name"='{new_name}',
                car_plate='{new_car_plate}',
                is_passenger={new_is_passenger},
                is_driver={new_is_driver},
                updated_at='{updated_at}'
                WHERE account_id='{old_id}'::uuid;
        """
        return sql.format(
            table=self.table,
            new_name=new_account.name,
            new_car_plate=new_account.car_plate,
            new_is_passenger=new_account.is_passenger,
            new_is_driver=new_account.is_driver,
            old_id=account.account_id,
            updated_at=datetime.now()
        )

    def _sql_update_password(self, account: Account, new_password):
        sql = """UPDATE {table} SET "password"='{new_password}', updated_at='{updated_at}'
            WHEERE account_id='{account_id}'::uuid;"""
        return sql.format(
            table=self.table, new_password=new_password, account_id=account.account_id, updated_at=datetime.now()
        )
