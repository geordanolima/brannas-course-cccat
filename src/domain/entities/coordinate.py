from src.domain.models.coordinate import Coordinate


class CoordinateEntitie(Coordinate):
    def __init__(self, latitude: float, longitude: float) -> None:
        self._coordinate = Coordinate()
        self._coordinate.latitude = latitude
        self._coordinate.longitude = longitude

    def object(self) -> Coordinate:
        return self._coordinate
