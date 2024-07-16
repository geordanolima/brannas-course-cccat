import re

from src.presenter import ErrorInvalidName

from ._base_value_object import BaseValueObject


class NameObject(BaseValueObject):
    def __init__(self, value) -> None:
        if self._validate(value=value):
            raise ErrorInvalidName()
        self._value = value

    def _validate(self, value):
        return not re.search(r"[a-zA-Z] [a-zA-Z]+", value)
