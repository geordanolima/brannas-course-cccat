import re

from src.presenter import ErrorInvalidEmail


class EmailObject():
    def __init__(self, value: str) -> None:
        if not self._validate(value=value):
            raise ErrorInvalidEmail()
        self._value = value

    def get_value(self) -> str:
        return self._value

    def _validate(self, value: str) -> bool:
        return re.search(r"^(.+)@(.+)$", value)
