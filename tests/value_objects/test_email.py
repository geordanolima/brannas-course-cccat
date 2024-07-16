import pytest

from src.domain.value_objects import EmailObject
from src.presenter import ErrorInvalidEmail


@pytest.mark.parametrize("email_input", ["email.com", "email", "email@@.com", "12345@email.com", "email@test"])
def test_email_invalid(email_input):
    with pytest.raises(ErrorInvalidEmail):
        email = EmailObject(email_input)
        email.get_value()


@pytest.mark.parametrize("email_input", ["email@email.com", "email_123@test.com", "email@test.com.br", "e.1_2@test.us"])
def test_email_valid(email_input):
    email = EmailObject(email_input)
    assert email.get_value() == email_input
