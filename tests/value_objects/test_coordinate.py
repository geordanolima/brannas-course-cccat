import pytest

from src.domain.value_objects import CoordinateObject
from src.presenter import ErrorCoordinateInvalid


@pytest.mark.parametrize("latitude_input,longitude_input", [
    (-91.39393, -2.122),
    (91.39393, -2.122),
    (-89.39393, -183.122),
    (-89.39393, 183.122),
])
def test_coordinate_invalid(latitude_input, longitude_input):
    with pytest.raises(ErrorCoordinateInvalid):
        coordinate = CoordinateObject(latitude=latitude_input, longitude=longitude_input)
        coordinate.object()


@pytest.mark.parametrize("latitude_input,longitude_input", [
    (-89.39393, -2.122),
    (89.39393, 2.122),
    (-89.39393, -177.122),
    (89.39393, 177.122),
])
def test_coordinate_valid(latitude_input, longitude_input):
    coordinate = CoordinateObject(latitude=latitude_input, longitude=longitude_input)
    assert coordinate.get_value().latitude == latitude_input
    assert coordinate.get_value().longitude == longitude_input
        