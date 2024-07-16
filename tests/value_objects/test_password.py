import pytest

from src.domain.value_objects import PasswordObject
from src.presenter.errors import ErrorPasswordNotAccept


@pytest.mark.parametrize("password_input", ["abcDeFgHijk", "12345678", "123456789012345678", "@@@@@@@@"])
def test_password_invalid(password_input):
    with pytest.raises(ErrorPasswordNotAccept):
        password = PasswordObject(password_input)
        password.get_value()


@pytest.mark.parametrize("password_input", ["Abcd@1234", "Password#123", "LongPassword$01"])
def test_password_valid(password_input):
    password = PasswordObject(password_input)
    assert password.get_value() != password_input
    assert PasswordObject().compare_password(password.get_value().encode(), password_input)
