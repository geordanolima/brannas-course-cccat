import re

from src.domain.entities.cpf import Cpf
from src.domain.models import Account
from src.presenter import (
    ErrorInvalidName,
    ErrorInvalidEmail,
    ErrorInvalidPlate,
)
from src.utils.passwords import Password


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
        if self.invalid_name(name=name):
            raise ErrorInvalidName()
        if self.invalid_email(email=email):
            raise ErrorInvalidEmail()
        if self.invalid_plate(plate=car_plate, is_driver=is_driver):
            raise ErrorInvalidPlate()
        password = Password().cryptography_password(password=password)
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

    @classmethod
    def invalid_name(self, name):
        return not re.search(r"[a-zA-Z] [a-zA-Z]+", name)

    @classmethod
    def invalid_email(self, email):
        return not re.search(r"^(.+)@(.+)$", email)

    @classmethod
    def invalid_plate(self, plate: str, is_driver: bool):
        if is_driver:
            plate = plate.replace("-", "")
            return not re.search(r"^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$", plate)
        return False

    def object(self, hide_password: bool = False):
        if hide_password:
            self._account.password = "**********"
        return self._account
