from src.domain.models import Coordinate
from src.presenter import ErrorCoordinateInvalid


class CoordinateObject:
    def __init__(self, latitude: float, longitude: float) -> None:
        if not(abs(latitude) <= 90 and abs(longitude) <= 180):
            raise ErrorCoordinateInvalid()
        self._value = Coordinate(latitude=latitude, longitude=longitude)

    def object(self) -> Coordinate:
        return self._value
