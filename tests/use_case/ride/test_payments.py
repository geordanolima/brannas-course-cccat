from uuid import uuid4
import pytest

from src.use_case import RidePayment
from src.domain.constants import RideStatusEnum
from src.presenter import ErrorIsInvalidUUID, ErrorRideNotFound, ErrorMissingInformation, ErrorStatusNotAllowed


def test_get_not_exists_ride(ride_repository, transaction_repository):
    with pytest.raises(ErrorIsInvalidUUID):
        use_case = RidePayment(ride_repository=ride_repository, transaction_repository=transaction_repository)
        use_case.run(ride_id="test", credit_card_token=None, amount=None)
        
        
def test_ride_not_existent(ride_repository, transaction_repository):
    with pytest.raises(ErrorRideNotFound):
        use_case = RidePayment(ride_repository=ride_repository, transaction_repository=transaction_repository)
        use_case.run(ride_id=str(uuid4()), credit_card_token=None, amount=None)


def test_fail_payment(ride_repository, transaction_repository, ride_pending_pay):
    with pytest.raises(ErrorMissingInformation):
        use_case = RidePayment(ride_repository=ride_repository, transaction_repository=transaction_repository)
        use_case.run(ride_id=ride_pending_pay.ride_id, credit_card_token=None, amount=None)


def test_status_not_allowed(ride_repository, transaction_repository, ride_in_progress):
    with pytest.raises(ErrorStatusNotAllowed):
        use_case = RidePayment(ride_repository=ride_repository, transaction_repository=transaction_repository)
        use_case.run(ride_id=ride_in_progress.ride_id, credit_card_token="in_progress", amount=123)


def test_success_payment(ride_repository, transaction_repository, ride_pending_pay):
    use_case = RidePayment(ride_repository=ride_repository, transaction_repository=transaction_repository)
    ride = use_case.run(ride_id=ride_pending_pay.ride_id, credit_card_token="Success", amount=123)
    assert ride.status == RideStatusEnum.PENDING_RATE.name
