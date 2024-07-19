from uuid import uuid4

import pytest

from src.domain.constants import RideStatusEnum
from src.domain.models import Ride
from src.presenter import (
    ErrorIsInvalidUUID,
    ErrorAccountNotFound,
    ErrorRideNotFound,
    ErrorIsNeedDriver,
    ErrorHaveRideInProgress,
    ErrorStatusNotAllowed,
)
from src.use_case import RideAccept


@pytest.fixture
def ride_in_progress(create_ride, ride_repository):
    ride_in_progress = Ride(**create_ride.dict())
    ride_in_progress.ride_id = str(uuid4())
    ride_in_progress.status = RideStatusEnum.IN_PROGRESS.value
    return ride_repository.insert_ride(ride=ride_in_progress)


def test_accept_ride_uuid_invalid(account_repository, ride_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id="invalid_uuid", ride_id="invalid_uuid")


def test_accept_ride_account_not_found(account_repository, ride_repository):
    with pytest.raises(ErrorAccountNotFound):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=str(uuid4()), ride_id=str(uuid4()))


def test_accept_ride_not_found(account_repository, ride_repository, account_driver):
    with pytest.raises(ErrorRideNotFound):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=str(uuid4()))


def test_accept_ride_is_not_driver(account_repository, ride_repository, account_passenger):
    with pytest.raises(ErrorIsNeedDriver):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_passenger.account_id, ride_id=str(uuid4()))


def test_accept_driver_have_other_ride(
    account_repository, ride_repository, account_driver, ride_in_progress, ride_created
):
    with pytest.raises(ErrorHaveRideInProgress):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_created.ride_id)


def test_accept_ride_status_not_alowed(account_repository, ride_repository, account_driver, ride_canceled):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
        use_case.run(driver_id=account_driver.account_id, ride_id=ride_canceled.ride_id)


def test_accept_ride_success(account_repository, ride_repository, account_driver, ride_created):
    use_case = RideAccept(account_repository=account_repository, ride_repository=ride_repository)
    ride = use_case.run(driver_id=account_driver.account_id, ride_id=ride_created.ride_id)
    assert ride.driver_id == account_driver.account_id
    assert ride.status == RideStatusEnum.ACCEPT.value
