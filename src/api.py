from fastapi import FastAPI, Response

from .controller.account_controller import AccountController

from .models.account import Account

app = FastAPI()


@app.get("/health", include_in_schema=False)
def simplehealth():
    return {"message": "OK"}


@app.post("/signup", tags=["account"], response_class=Response)
def signup(account: Account):
    controller = AccountController()
    return controller.run(account=account)
