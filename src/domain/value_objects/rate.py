import re

from src.presenter import ErrorInvalidRate

from ._base_value_object import BaseValueObject


class RateObject(BaseValueObject):
    def __init__(self, value: int) -> None:
        self._value = -1
        if not self._validate(value=value):
            raise ErrorInvalidRate()
        self._value = value
        
    def _validate(self, value):
        return re.search(r"^[0-5]$", str(value))
