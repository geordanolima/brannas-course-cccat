import pytest

from src.domain.value_objects import CarPlateObject
from src.presenter import ErrorInvalidPlate


@pytest.mark.parametrize("plate_input", ["AAA-AAAA", "111-1111", "@@@-@@@@", "111-AAAA"])
def test_invalid_car_plate(plate_input):
    with pytest.raises(ErrorInvalidPlate):
        CarPlateObject(True, plate_input).get_value()


def test_invalid_car_plate_is_driver_false():
    plate = "@@@-1234"
    valid_plate = CarPlateObject(False, plate).get_value()
    assert valid_plate == ''


@pytest.mark.parametrize("plate_input", ["ABC-1234", "ABC-1D23", "abc-1234", "abc-1d23", "abc1234",  "abc1d23"])
def test_success_car_plate(plate_input):
    valid_plate = CarPlateObject(True, plate_input).get_value()
    assert valid_plate == plate_input
