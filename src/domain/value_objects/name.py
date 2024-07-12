import re

from src.presenter import ErrorInvalidName


class NameObject:
    def __init__(self, value) -> None:
        if self._validate(value=value):
            raise ErrorInvalidName()
        self._value = value

    def get_value(self) -> str:
        return self._value

    def _validate(self, value):
        return not re.search(r"[a-zA-Z] [a-zA-Z]+", value)
