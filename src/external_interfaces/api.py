from fastapi import FastAPI, Response

from ..controller import AccountController, RideController
from ..domain.models import Account, LoginRequest, RideRequest, RideUpdateStatusRequest

app = FastAPI()


@app.get("/health", include_in_schema=False)
def simplehealth():
    return {"message": "OK"}


@app.post("/signup", tags=["account"], response_class=Response)
def signup(account: Account):
    controller = AccountController()
    return controller.create_account(account=account)


@app.post("/login", tags=["account"], response_class=Response)
def login(login: LoginRequest):
    controller = AccountController()
    return controller.login(login=login)


@app.get("/account/{account_id}", tags=["account"], response_class=Response)
def get_account(account_id: str):
    controller = AccountController()
    return controller.get_account_by_id(account_id=account_id)


@app.post("/ride", tags=["passenger"], response_class=Response)
def ride(ride: RideRequest):
    controller = RideController()
    return controller.create_ride(
        account=ride.passenger_id, from_coordinate=ride.from_coordinate, to_coordinate=ride.to_coordinate
    )


@app.patch("/ride/accept", tags=["passenger"], response_class=Response)
def ride_accept(ride_accept: RideUpdateStatusRequest):
    controller = RideController()
    return controller.accept_ride(ride_id=ride_accept.ride_id, driver_id=ride_accept.driver_id)


@app.get("/ride/{ride_id}", tags=["passenger"], response_class=Response)
def ride_by_id(ride_id: str):
    controller = RideController()
    return controller.get_ride(ride_id=ride_id)
