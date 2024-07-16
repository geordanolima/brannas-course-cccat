from uuid import uuid4

from pydantic import BaseModel


class Account(BaseModel):
    account_id: str = str(uuid4())
    name: str
    email: str
    password: str
    cpf: str
    is_passenger: bool
    rate: int
    is_driver: bool | None = False
    car_plate: str | None
    created_at: str | None
    updated_at: str | None
