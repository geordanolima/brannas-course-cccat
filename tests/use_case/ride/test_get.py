import pytest

from src.presenter import ErrorIsInvalidUUID
from src.use_case import RideGet


def test_get_not_exists_ride(create_ride, ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideGet(ride_repository=ride_repository)
        use_case.get_id(id=create_ride.ride_id)


def test_get_exists_ride(ride_repository, ride_created):
    use_case = RideGet(ride_repository=ride_repository)
    ride = use_case.get_id(id=ride_created.ride_id)
    assert ride == ride_created
