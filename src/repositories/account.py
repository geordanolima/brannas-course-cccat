from src.models.account import Account


class AccountRepository():
    table: str = "account"
    
    def __init__(self, account: Account = None) -> None:
        self.account = account
        
    def sql_create_account(self) -> str:
        sql = """INSERT INTO {table} (account_id, "name", email, cpf, car_plate, is_passenger, is_driver)
            VALUES ('{account_id}', '{name}', '{email}', '{cpf}', '{car_plate}', {is_passenger}, {is_driver});
        """
        return sql.format(
            table=self.table,
            account_id=self.account.account_id,
            name=self.account.name,
            email=self.account.email,
            cpf=self.account.cpf,
            car_plate=self.account.car_plate,
            is_passenger=self.account.is_passenger,
            is_driver=self.account.is_driver,
        )

    def get_exists_account(self, email):
        return f"select count(1) from {self.table} where email = '{email}';"
    
    def get_account_email(self, email):
        return f"select * from {self.table} where email = '{email}';"
    
    def get_account_id(self, id):
        return f"select * from {self.table} where account_id = '{id}';"
    
    def get_accounts(self, limit: int = None):
        query_limit = ""
        if limit:
            query_limit = f"LIMIT {limit}"
        return f"select * from {self.table} {query_limit}';"
