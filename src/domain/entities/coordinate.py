from src.domain.models.coordinate import Coordinate


class CoordinateEntitie:
    def __init__(self, latitude: float, longitude: float) -> None:
        self._coordinate = Coordinate(latitude=latitude, longitude=longitude)

    def object(self) -> Coordinate:
        return self._coordinate
