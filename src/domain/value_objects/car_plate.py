import re

from src.presenter import ErrorInvalidPlate

from ._base_value_object import BaseValueObject


class CarPlateObject(BaseValueObject):
    def __init__(self, is_driver: bool, value: str) -> None:
        self._value = ""
        if is_driver and not self._validate(value=value):
            raise ErrorInvalidPlate()
        if is_driver:
            self._value = value

    def _validate(self, value: str) -> bool:
        return re.search(r"^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$", value.replace("-", ""))
