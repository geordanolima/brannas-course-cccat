from src.domain.constants import RideStatusEnum
from src.domain.repositories import RideRepository, PositionRepository
from src.domain.value_objects import SegmentObject
from src.presenter import ErrorRideNotFound, ErrorStatusNotAllowed
from src.use_case import BaseUseCase


class RideFinish(BaseUseCase):
    def __init__(self, ride_repository: RideRepository, position_repository: PositionRepository) -> None:
        super().__init__()
        self._ride_repository = ride_repository
        self._position_repository = position_repository
        self.status = RideStatusEnum.PENDING_PAY.value
        self.fare_for_km = 2.1

    def run(self, ride_id: str):
        self._validate_id(id=ride_id)
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if not ride.validate_next_state(new_status=self.status):
            raise ErrorStatusNotAllowed()
        positions = self._position_repository.get_position_by_ride(ride_id=ride_id)
        distance = self._calculate_distance(positions=positions)
        fare = distance * self.fare_for_km
        return self._ride_repository.update_fare_ride(ride=ride, fare=fare, distance=distance, new_status=self.status)

    def _calculate_distance(self, positions):
        distance = 0
        for indice in range(len(positions) - 1):
            segment = SegmentObject(coordinate_from=positions[indice], coordinate_to=positions[indice + 1])
            distance += segment.get_value()
        return distance
