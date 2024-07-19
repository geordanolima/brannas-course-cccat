from pydantic import BaseModel


class RideUpdateStatusRequest(BaseModel):
    driver_id: str
    ride_id: str
