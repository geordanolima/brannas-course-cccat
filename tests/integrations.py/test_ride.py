from fastapi import status

from src.controller import RideController

def test_ride_process(
    db_clear, ride_controller: RideController, populate_account, populate_account_driver, from_coordinate, to_coordinate, positions
):
    ride = ride_controller.create_ride(
        account=populate_account.account_id, from_coordinate=from_coordinate, to_coordinate=to_coordinate
    )
    assert ride.status_code == status.HTTP_200_OK
    ride = eval(ride.body.decode().replace('null', 'None'))
    ride_accept = ride_controller.accept_ride(ride_id=ride.get('ride_id'), driver_id=populate_account_driver.account_id)
    assert ride_accept.status_code == status.HTTP_200_OK
    ride_started = ride_controller.start_ride(ride_id=ride.get('ride_id'), driver_id=populate_account_driver.account_id)
    assert ride_started.status_code == status.HTTP_200_OK
    for position in positions:
        ride_position = ride_controller.update_position(ride_id=ride.get('ride_id'), coordinate=position)
        assert ride_position.status_code == status.HTTP_200_OK
    ride_finished = ride_controller.finish_ride(ride_id=ride.get('ride_id'))
    assert ride_finished.status_code == status.HTTP_200_OK
    ride_finished = eval(ride_finished.body.decode().replace('null', 'None'))
    assert ride_finished.get('distance') == float(39505.0)
