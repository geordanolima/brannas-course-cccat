import pytest

from src.domain.value_objects import CoordinateObject, SegmentObject


@pytest.fixture
def initial_coordinate():
    return CoordinateObject(latitude=-27.584905257808835, longitude=-48.545022195325124).get_value()


@pytest.fixture
def end_coordinate():
    return CoordinateObject(latitude=-27.496887588317275, longitude=-48.522234807851476).get_value()


def test_valid_seguiment(initial_coordinate, end_coordinate):
    segment = SegmentObject(initial_coordinate, end_coordinate)
    assert segment.get_value() == 10
