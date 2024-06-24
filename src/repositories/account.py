from curso_brannas.src.models.account import Account


class AccountRepository():
    table: str = "account"
    
    def __init__(self, account: Account = None) -> None:
        self.account = account
        
    def sql_create_account(self) -> str:
        sql = """INSERT INTO account (account_id, "name", email, cpf, car_plate, is_passenger, is_driver)
            VALUES ('{id}', '{name}', '{email}', '{cpf}', '{car_plate}', {is_passenger}, {is_driver});
        """
        return sql.format(
            id=self.account.get_id(),
            name=self.account.name,
            email=self.account.email,
            cpf=self.account.cpf,
            car_plate=self.account.car_plate,
            is_passenger=self.account.is_passenger,
            is_driver=self.account.is_driver,
        )

    def get_exists_account(self, email):
        return f"select count(1) from {self.table} where email = '{email}'"
    
    def get_account(self, email):
        return f"select * from {self.table} where email = '{email}'"