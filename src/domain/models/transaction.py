from pydantic import BaseModel

from src.addapters.machine_status import MachineStatus
from src.domain.constants import TransactionStatusEnum


class Transaction(BaseModel):
    transaction_id: str
    ride_id: str
    amount: float
    status: int
    created_at: str

    def _machine_status(self):
        return [
            {
                "current_status": TransactionStatusEnum.CREATED, "permitted_next_status": [
                    TransactionStatusEnum.FAIL, TransactionStatusEnum.SUCCESS
                ]
            },
            {
                "current_status": TransactionStatusEnum.SUCCESS, "permitted_next_status": []
            },
            {
                "current_status": TransactionStatusEnum.FAIL, "permitted_next_status": []
            },
        ]

    def validate_next_state(self, new_status: int):
        machine = MachineStatus(machine_status=self._machine_status())
        return machine.validate_next_status(current_status=self.status, new_status=new_status)
