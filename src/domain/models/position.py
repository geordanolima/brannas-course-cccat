from datetime import datetime

from pydantic import BaseModel


class Position(BaseModel):
    position_id: str
    ride_id: str
    latitude: float
    longitude: float
    created_at: str
