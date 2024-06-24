import uuid


class Account():
    id: str
    name: str
    email: str
    cpf: str
    is_passenger: bool 
    is_driver: bool
    car_plate: str

    def get_id(self):
        return uuid.uuid4()

    def new(self, **kwargs):
        def _validate(value):
            return value if len(str(value)) else "Null"
        self.name = _validate(kwargs["name"])
        self.email = _validate(kwargs["email"])
        self.cpf = _validate(kwargs["cpf"])
        self.is_passenger = _validate(kwargs["is_passenger"])
        self.is_driver = _validate(kwargs["is_driver"])
        self.car_plate = _validate(kwargs["car_plate"])
