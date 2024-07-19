from math import sin, cos, pi, atan2, sqrt

from src.presenter import ErrorInvalidSegment
from src.domain.models import Coordinate

from ._base_value_object import BaseValueObject


class SegmentObject(BaseValueObject):
    def __init__(self, coordinate_from: Coordinate, coordinate_to: Coordinate):
        if not coordinate_from or not coordinate_to:
            raise ErrorInvalidSegment()
        self._value = self._get_distance(coordinate_from, coordinate_to)

    def _get_distance(self, coordinate_from, coordinate_to):
        """ method to calculate distance between two points """
        earth_radius = 6371
        degrees_to_radians = pi / 180
        delta_latitude = (coordinate_to.latitude - coordinate_from.latitude) * degrees_to_radians
        delta_longitude = (coordinate_to.longitude - coordinate_from.longitude) * degrees_to_radians
        sin_lat = sin(delta_latitude / 2) * sin(delta_latitude / 2)
        cos_lat_from = cos(coordinate_from.latitude * degrees_to_radians)
        cos_lat_to = cos(
            coordinate_to.latitude * degrees_to_radians
        )
        sin_lon = sin(delta_longitude / 2)
        calc = sin_lat + cos_lat_from * cos_lat_to * sin_lon * sin_lon
        c = 2 * atan2(sqrt(calc), sqrt(1 - calc))
        distance = earth_radius * c
        return round(distance)
