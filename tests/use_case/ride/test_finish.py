from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.entities import PositionEntitie
from src.domain.value_objects import CoordinateObject
from src.presenter import ErrorIsInvalidUUID, ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import RideFinish


@pytest.fixture
def positions_insert(position_repository, ride_in_progress):
    coordinates = [
        CoordinateObject(latitude=-30.853844, longitude=-51.810560).get_value(),
        CoordinateObject(latitude=-30.853490, longitude=-51.802633).get_value(),
        CoordinateObject(latitude=-30.854396, longitude=-51.800137).get_value(),
        CoordinateObject(latitude=-30.855200, longitude=-51.797964).get_value(),
        CoordinateObject(latitude=-30.855558, longitude=-51.793501).get_value(),
        CoordinateObject(latitude=-30.858618, longitude=-51.788213).get_value(),
        CoordinateObject(latitude=-30.874391, longitude=-51.812511).get_value(),
    ]
    for coordinate in coordinates:
        position = PositionEntitie(position_id=str(uuid4()), ride_id=ride_in_progress.ride_id, coordinate=coordinate)
        position_repository.insert_position(position=position.object())
    return {"distance": 5, "fare": 10.5}


def test_finish_ride_uuid_invalid(position_repository, ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideFinish(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id="invalid_uuid")


def test_finish_ride_not_found(position_repository, ride_repository):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideFinish(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=str(uuid4()))


def test_finish_ride_status_not_alowed(position_repository, ride_repository, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideFinish(ride_repository=ride_repository, position_repository=position_repository)
        use_case.run(ride_id=ride_canceled.ride_id)


def test_success_finish_ride(position_repository, ride_repository, ride_in_progress, positions_insert):
    use_case = RideFinish(ride_repository=ride_repository, position_repository=position_repository)
    ride = use_case.run(ride_id=ride_in_progress.ride_id)
    assert ride.status == RideStatusEnum.PENDING_PAY.value
    assert ride.distance == positions_insert.get("distance")
    assert ride.fare == positions_insert.get("fare")
