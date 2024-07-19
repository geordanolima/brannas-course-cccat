from src.domain.constants import RideStatusEnum, TransactionStatusEnum
from src.domain.entities import TransactionEntitie
from src.domain.repositories import RideRepository, TransactionRepository
from src.presenter import ErrorMissingInformation, ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import BaseUseCase


class RidePayment(BaseUseCase):
    def __init__(self, ride_repository: RideRepository, transaction_repository: TransactionRepository) -> None:
        self._ride_repository = ride_repository
        self._transaction_repository = transaction_repository
        self._status = RideStatusEnum.PENDING_RATE.value

    def run(self, ride_id: str, credit_card_token: str, amount: float):
        self._validate_id(ride_id)
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if not credit_card_token and not amount:
            raise ErrorMissingInformation()
        if not ride.validate_next_state(new_status=self._status):
            raise ErrorStatusNotAllowed()
        # transaction, always returns success
        transaction = TransactionEntitie(
            ride_id=ride_id, amount=amount, status=TransactionStatusEnum.SUCCESS.value
        ).object()
        self._transaction_repository.insert_transaction(transaction=transaction)
        return self._ride_repository.update_status_ride(ride=ride, new_status=self._status)
