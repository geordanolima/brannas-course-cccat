
class _Coordinate:
    latitude: float
    longitude: float


class CoordinateEntitie(_Coordinate):
    def __init__(self, latitude: float, longitude: float) -> None:
        self._coordinate = _Coordinate()
        self._coordinate.latitude = latitude
        self._coordinate.longitude = longitude

    def object(self) -> _Coordinate:
        return self._coordinate
