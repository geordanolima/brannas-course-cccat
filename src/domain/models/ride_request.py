from pydantic import BaseModel

from src.domain.models.coordinate import Coordinate


class RideRequest(BaseModel):
    passenger_id: str
    from_coordinate: Coordinate
    to_coordinate: Coordinate
