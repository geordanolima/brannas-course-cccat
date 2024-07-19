from datetime import datetime
from uuid import uuid4

from src.domain.constants import TransactionStatusEnum
from src.domain.models import Transaction
from ._base_entitie import BaseEntitie

class TransactionEntitie(BaseEntitie):
    def __init__(
        self,
        ride_id: str,
        amount: float,
        transaction_id: str = str(uuid4()),
        status: int = TransactionStatusEnum.CREATED.value,
        created_at: str = datetime.now().isoformat(),
    ) -> None:
        self._value = Transaction(
            transaction_id=transaction_id,
            ride_id=ride_id,
            amount=amount,
            status=status,
            created_at=created_at,
        )
