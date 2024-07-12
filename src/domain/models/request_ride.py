from pydantic import BaseModel

from src.domain.models import Coordinate


class RideRequest(BaseModel):
    passenger_id: str
    from_coordinate: Coordinate
    to_coordinate: Coordinate


class RideUpdateStatusRequest(BaseModel):
    driver_id: str
    ride_id: str


class RideAddPositionRequest(BaseModel):
    ride_id: str
    coordinate: Coordinate
