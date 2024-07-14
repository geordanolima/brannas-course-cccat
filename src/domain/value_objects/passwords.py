import re

import bcrypt

from src.presenter.errors import ErrorPasswordNotAccept

from ._base_value_object import BaseValueObject


class PasswordObject(BaseValueObject):
    def __init__(self, value: str = "") -> None:
        if value and not self._validate(value):
            raise ErrorPasswordNotAccept()
        self._value = self._cryptography_password(value)

    def _validate(self, value: str) -> bool:
        return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$', value)

    def _cryptography_password(self, value: str):
        value = value.encode("utf-8")
        return bcrypt.hashpw(value, bcrypt.gensalt(5)).decode()

    @classmethod
    def compare_password(self, hashed_password, password):
        password = password.encode("utf-8")
        return bcrypt.checkpw(password=password, hashed_password=hashed_password)
