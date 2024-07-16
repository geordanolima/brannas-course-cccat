from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.models import Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorRideOfOtherDriver,
    ErrorRideNotFound,
    ErrorStatusNotAllowed,
)
from src.use_case import RideStart


@pytest.fixture
def ride_accept_other_driver(create_ride, ride_repository):
    ride_accept_other_driver = Ride(**create_ride.dict())
    ride_accept_other_driver.ride_id = str(uuid4())
    ride_accept_other_driver.driver_id = str(uuid4())
    ride_accept_other_driver.status = RideStatusEnum.ACCEPT.value
    return ride_repository.insert_ride(ride=ride_accept_other_driver)


@pytest.fixture
def ride_accept(create_ride, ride_repository):
    ride_accept = Ride(**create_ride.dict())
    ride_accept.ride_id = str(uuid4())
    ride_accept.status = RideStatusEnum.ACCEPT.value
    return ride_repository.insert_ride(ride=ride_accept)


@pytest.fixture
def ride_canceled(create_ride, ride_repository):
    ride_status_not_allowed = Ride(**create_ride.dict())
    ride_status_not_allowed.ride_id = str(uuid4())
    ride_status_not_allowed.status = RideStatusEnum.CANCELED.value
    return ride_repository.insert_ride(ride=ride_status_not_allowed)


def test_accept_ride_uuid_invalid(ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id="invalid_uuid", ride_id="invalid_uuid")


def test_accept_ride_not_found(ride_repository, account_driver):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=str(uuid4()))


def test_accept_ride_is_not_driver(ride_repository, account_passenger, ride_accept_other_driver):
    with pytest.raises(ErrorRideOfOtherDriver):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_passenger.account_id, ride_id=ride_accept_other_driver.ride_id)


def test_accept_ride_status_not_alowed(ride_repository, account_driver, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideStart(ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_canceled.ride_id)


def test_start_ride_success(ride_repository, account_driver, ride_accept):
    use_case = RideStart(ride_repository=ride_repository)
    ride = use_case.run(driver_id=account_driver.account_id, ride_id=ride_accept.ride_id)
    assert ride.driver_id == account_driver.account_id
    assert ride.status == RideStatusEnum.IN_PROGRESS.name
