from uuid import uuid4

from pydantic import BaseModel

from addapters.machine_status import MachineStatus

from ..constants import RideStatusEnum


class Ride(BaseModel):
    ride_id: str = uuid4()
    passenger_id: str
    driver_id: str
    status: int = RideStatusEnum.CREATED
    fare: float
    distance: float
    from_lat: float
    from_long: float
    to_lat: float
    to_long: float
    date: float

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
