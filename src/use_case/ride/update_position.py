from uuid import uuid4
from src.presenter import ErrorRideNotFound, ErrorStatusNotAllowed

from src.domain.constants import RideStatusEnum
from src.domain.entities import PositionEntitie
from src.domain.models import Position
from src.domain.repositories import PositionRepository, RideRepository
from src.domain.value_objects import CoordinateObject
from src.use_case import BaseUseCase


class RideUpdatePosition(BaseUseCase):
    def __init__(self, ride_repository: RideRepository, position_repository: PositionRepository) -> None:
        self._ride_repository = ride_repository
        self._position_repository = position_repository

    def run(self, ride_id: str, coordinate: CoordinateObject) -> Position:
        self._validate_id(id=ride_id)
        ride = self._ride_repository.get_ride_by_id(id=ride_id)
        if not ride:
            raise ErrorRideNotFound()
        if ride.status != RideStatusEnum.IN_PROGRESS.value:
            raise ErrorStatusNotAllowed()
        position = PositionEntitie(position_id=str(uuid4()), ride_id=ride_id, coordinate=coordinate).object()
        return self._position_repository.insert_position(position=position)
