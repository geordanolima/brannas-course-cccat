from fastapi import FastAPI

from src.external_interfaces.routes import account, ride

app = FastAPI()


@app.get("/health", include_in_schema=False)
def simplehealth():
    return {"message": "OK"}


app.include_router(account.router)
app.include_router(ride.router)
