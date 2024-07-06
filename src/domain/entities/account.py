from .cpf import Cpf
from src.domain.models import Account


class AccountEntitie:
    def __init__(
        self,
        account_id: str,
        name: str,
        email: str,
        password: str,
        cpf: str,
        car_plate: str,
        is_passenger: bool = False,
        is_driver: bool = False,
    ):
        self._account = Account(
            account_id=account_id,
            name=name,
            email=email,
            password=password,
            cpf=Cpf(cpf).get_cpf(),
            is_passenger=is_passenger,
            is_driver=is_driver,
            car_plate=car_plate,
        )

    def object(self, hide_password: bool = False):
        if hide_password:
            self._account.password = "**********"
        return self._account
