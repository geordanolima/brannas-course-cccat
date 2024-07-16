from math import sin, cos, pi, atan2, sqrt

from src.domain.models import Coordinate

from ._base_value_object import BaseValueObject


class SegmentObject(BaseValueObject):
    def __init__(self, coordinate_from: Coordinate, coordinate_to: Coordinate):
        if not coordinate_from or not coordinate_to:
            raise ValueError("Invalid segment")
        self.coordinate_from = coordinate_from
        self.coordinate_to = coordinate_to
        self._value = self._get_distance()

    def _get_distance(self):
        """ method to calculate distance between two points """
        earth_radius = 6371
        degrees_to_radians = pi / 180
        delta_latitude = (self.coordinate_to.latitude - self.coordinate_from.latitude) * degrees_to_radians
        delta_longitude = (self.coordinate_to.longitude - self.coordinate_from.longitude) * degrees_to_radians
        sin_lat = sin(delta_latitude / 2) * sin(delta_latitude / 2)
        cos_lat_from = cos(self.coordinate_from.latitude * degrees_to_radians)
        cos_lat_to = cos(
            self.coordinate_to.latitude * degrees_to_radians
        )
        sin_lon = sin(delta_longitude / 2)
        calc = sin_lat + cos_lat_from * cos_lat_to * sin_lon * sin_lon
        c = 2 * atan2(sqrt(calc), sqrt(1 - calc))
        distance = earth_radius * c
        return round(distance)
