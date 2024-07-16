from fastapi import APIRouter, Response

from src.domain.models import RideRequest, RideUpdateStatusRequest, RideAddPositionRequest
from src.controller import RideController

_controller = RideController()

router = APIRouter(prefix="/ride", tags=["ride"], default_response_class=Response)


@router.post("/")
def ride(ride: RideRequest):
    return _controller.create_ride(
        account=ride.passenger_id, from_coordinate=ride.from_coordinate, to_coordinate=ride.to_coordinate
    )


@router.patch("/accept")
def ride_accept(ride_accept: RideUpdateStatusRequest):
    return _controller.accept_ride(ride_id=ride_accept.ride_id, driver_id=ride_accept.driver_id)


@router.patch("/start")
def ride_start(ride_start: RideUpdateStatusRequest):
    return _controller.start_ride(ride_id=ride_start.ride_id, driver_id=ride_start.driver_id)


@router.patch("/{ride_id}/finish")
def finish_ride(ride_id: str):
    return _controller.finish_ride(ride_id=ride_id)


@router.post("/position")
def create_new_position(position: RideAddPositionRequest):
    controller = RideController()
    return controller.update_position(ride_id=position.ride_id, coordinate=position.coordinate)


@router.get("/{ride_id}")
def ride_by_id(ride_id: str):
    return _controller.get_ride(id=ride_id)
