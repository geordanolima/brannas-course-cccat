import pytest

from src.domain.value_objects import NameObject
from src.presenter import ErrorInvalidName

@pytest.mark.parametrize("name_input", ["nametest", "name12345 ", " nametest", "name 1243asa"])
def test_name_invalid(name_input):
    with pytest.raises(ErrorInvalidName):
        name = NameObject(name_input)
        name.get_value()


@pytest.mark.parametrize("name_input", ["name test", "name test othername"])
def test_name_valid(name_input):
    name = NameObject(name_input)
    assert name.get_value() == name_input
