from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.models import Coordinate, Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorRideNotFound,
    ErrorStatusNotAllowed,
)
from src.use_case import RideUpdatePosition
from tests.repositories import PositionTestRepository


@pytest.fixture
def position_repository() -> PositionTestRepository:
    return PositionTestRepository(db=None)


@pytest.fixture
def ride_in_progress(create_ride, ride_repository):
    ride_in_progress = Ride(**create_ride.dict())
    ride_in_progress.ride_id = str(uuid4())
    ride_in_progress.status = RideStatusEnum.IN_PROGRESS.value
    return ride_repository.insert_ride(ride=ride_in_progress)


def test_update_positon_uuid_invalid(ride_repository, position_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id="invalid_uuid", coordinate=Coordinate(latitude=10, longitude=11))


def test_update_position_ride_not_found(ride_repository, position_repository):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=str(uuid4()), coordinate=Coordinate(latitude=10, longitude=11))


def test_update_position_status_not_allwed(ride_repository, position_repository, ride_created):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=ride_created.ride_id, coordinate=Coordinate(latitude=10, longitude=11))


def test_success_update_position(ride_repository, position_repository, ride_in_progress):
    use_case = RideUpdatePosition(ride_repository=ride_repository, position_repository=position_repository)
    position = use_case.run(ride_id=ride_in_progress.ride_id, coordinate=Coordinate(latitude=10, longitude=11))
    assert position.position_id is not None
    assert position.latitude == 10
    assert position.longitude == 11
