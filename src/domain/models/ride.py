from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel

from ..constants import RideStatusEnum
from ...addapters.machine_status import MachineStatus


class Ride(BaseModel):
    ride_id: str = uuid4()
    passenger_id: str
    driver_id: str | None
    status: int = RideStatusEnum.CREATED.value
    fare: float | None
    distance: float | None
    from_latitudeitude: float | None
    from_longitudeitude: float | None
    to_latitudeitude: float | None
    to_longitude: float | None
    date: datetime | None

    MACHINE_STATUS = [
        {
            "current_status": RideStatusEnum.CREATED, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.PENDING_ACCEPT
            ]
        },
        {
            "current_status": RideStatusEnum.PENDING_ACCEPT, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.ACCEPT
            ]
        },
        {
            "current_status": RideStatusEnum.ACCEPT, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.IN_PROGRESS
            ]
        },
        {
            "current_status": RideStatusEnum.IN_PROGRESS, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.PENDING_PAY
            ]
        },
        {
            "current_status": RideStatusEnum.PENDING_PAY, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.PAY_FAIL, RideStatusEnum.PENDING_RATE
            ]
        },
        {
            "current_status": RideStatusEnum.PENDING_RATE, "permitted_next_status": [
                RideStatusEnum.ERROR, RideStatusEnum.CANCELED, RideStatusEnum.FINISHED
            ]
        },
        {"current_status": RideStatusEnum.PAY_FAIL, "permitted_next_status": [RideStatusEnum.PENDING_PAY]},
        {"current_status": RideStatusEnum.FINISHED, "permitted_next_status": []},
        {"current_status": RideStatusEnum.CANCELED, "permitted_next_status": []},
        {"current_status": RideStatusEnum.ERROR, "permitted_next_status": []},
    ]

    def validate_next_state(self, new_status: RideStatusEnum):
        machine = MachineStatus(machine_status=self.MACHINE_STATUS)
        return machine.validate_next_status(current_status=self.status, new_status=new_status)
