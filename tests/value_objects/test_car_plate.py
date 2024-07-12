import pytest

from src.domain.value_objects import CarPlateObject
from src.presenter import ErrorInvalidPlate


def test_invalid_car_plate_only_letters():
    with pytest.raises(ErrorInvalidPlate):
        plate = "AAA-AAAA"
        CarPlateObject(True, plate).get_value()


def test_invalid_car_plate_only_numbers():
    with pytest.raises(ErrorInvalidPlate):
        plate = "111-1111"
        CarPlateObject(True, plate).get_value()


def test_invalid_car_plate_expecial_character():
    with pytest.raises(ErrorInvalidPlate):
        plate = "@@@-1234"
        CarPlateObject(True, plate).get_value()


def test_invalid_car_plate_is_driver_false():
    plate = "@@@-1234"
    valid_plate = CarPlateObject(False, plate).get_value()
    assert valid_plate == ''


def test_success_car_plate():
    plate = "ABC-1234"
    valid_plate = CarPlateObject(True, plate).get_value()
    assert valid_plate == plate


def test_success_car_plate_mercosul():
    plate = "ABC-1A34"
    valid_plate = CarPlateObject(True, plate).get_value()
    assert valid_plate == plate
