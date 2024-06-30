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
            cpf=cpf,
            is_passenger=is_passenger,
            is_driver=is_driver,
            car_plate=car_plate,
        )

    def object(self):
        return self._account
