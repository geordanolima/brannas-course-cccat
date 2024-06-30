from pydantic import BaseModel

from src.domain.models.coordinate import Coordinate


class RideRequest(BaseModel):
    account_id: str
    from_coordinate: Coordinate
    to_coordinate: Coordinate
