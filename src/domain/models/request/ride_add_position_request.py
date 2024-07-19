from pydantic import BaseModel

from src.domain.models import Coordinate


class RideAddPositionRequest(BaseModel):
    ride_id: str
    coordinate: Coordinate
