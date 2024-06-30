from fastapi import FastAPI, Response

from .controller import AccountController, RideController
from .domain.models import Account, RideRequest

app = FastAPI()


@app.get("/health", include_in_schema=False)
def simplehealth():
    return {"message": "OK"}


@app.post("/signup", tags=["account"], response_class=Response)
def signup(account: Account):
    controller = AccountController()
    return controller.run(account=account)


@app.post("/ride", tags=["passenger"], response_class=Response)
def ride(ride: RideRequest):
    controller = RideController()
    return controller.run(
        account=ride.account_id, from_coordinate=ride.from_coordinate, to_coordinate=ride.to_coordinate
    )
