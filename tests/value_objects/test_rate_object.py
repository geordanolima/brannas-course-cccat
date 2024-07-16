import pytest

from src.domain.value_objects import RateObject
from src.presenter import ErrorInvalidRate


@pytest.mark.parametrize("rate_input", ["a", -1, 6, 99])
def test_invalid_rate(rate_input):
    with pytest.raises(ErrorInvalidRate):
        rate = RateObject(rate_input)
        rate.get_value()


@pytest.mark.parametrize("rate_input", [1, 2, 3, 4, 5])
def test_valid_rate(rate_input):
    rate = RateObject(rate_input)
    assert rate.get_value() == rate_input
