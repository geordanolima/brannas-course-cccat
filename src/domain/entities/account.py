from datetime import datetime
from ._base_entitie import BaseEntitie

from src.domain.models import Account

from src.domain.value_objects import CarPlateObject, CpfObject, EmailObject, NameObject, PasswordObject


class AccountEntitie(BaseEntitie):
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
        created_at: datetime = datetime.now(),
        updated_at: datetime = None
    ):
        self._value = Account(
            account_id=account_id,
            name=NameObject(name).get_value(),
            email=EmailObject(email).get_value(),
            password=PasswordObject(password).get_value(),
            cpf=CpfObject(cpf).get_value(),
            is_passenger=is_passenger,
            is_driver=is_driver,
            car_plate=CarPlateObject(is_driver=is_driver, value=car_plate).get_value(),
            created_at=created_at,
            updated_at=updated_at,
        )
