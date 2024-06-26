from uuid import uuid4
from pydantic import BaseModel


class Account(BaseModel):
    account_id: str = uuid4()
    name: str
    email: str
    cpf: str
    is_passenger: bool
    is_driver: bool | None = False
    car_plate: str | None = ''    

    def get_id(self):
        return uuid4()


class AccountDict():
    def __init__(self, account_id, name, email, cpf, is_passenger, is_driver=False, car_plate=''):
        self._account = Account(
            account_id = account_id,
            name = name,
            email = email,
            cpf = cpf,
            is_passenger = is_passenger,
            is_driver = is_driver,
            car_plate = car_plate,
        )

    def account(self):
        return self._account