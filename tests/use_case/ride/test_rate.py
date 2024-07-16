from uuid import uuid4
import pytest

from src.domain.constants import RideStatusEnum
from src.presenter import ErrorIsInvalidUUID, ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import RideRate


def test_create_rate_invalid_uuid(ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideRate(ride_repository=ride_repository)
        use_case.run(ride_id="invalid uuid", rate=1)


def test_create_rate_ride_not_found(ride_repository):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideRate(ride_repository=ride_repository)
        use_case.run(ride_id=str(uuid4()), rate=1)


def test_create_rate_when_next_status_is_invalid(ride_repository, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideRate(ride_repository=ride_repository)
        use_case.run(ride_id=ride_canceled.ride_id, rate=1)


def test_create_rate_success(ride_repository, ride_pending_rate):
    use_case = RideRate(ride_repository=ride_repository)
    ride = use_case.run(ride_id=ride_pending_rate.ride_id, rate=5)
    assert ride.status == RideStatusEnum.FINISHED.value
    assert ride.rate == 5
